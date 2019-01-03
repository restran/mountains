# -*- coding: utf-8 -*-
# Created by restran on 2018/6/5
from __future__ import unicode_literals, absolute_import

import logging
import time
from ..encoding import force_text

try:
    import paramiko
except ImportError:
    raise Exception('paramiko is not installed')

logger = logging.getLogger(__name__)


class SSHClient(object):
    def __init__(self, host, port, username, password=None, key_file=None,
                 key_pass=None, show_output=True, manual_connect=False, timeout=10):
        self.is_root = False
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.ssh_session = paramiko.SSHClient()
        self.ssh_session.load_system_host_keys()
        self.key_file = key_file
        self.key_pass = key_pass
        self.ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.private_key = None
        self.sftp = None
        self.show_output = show_output
        self.timeout = timeout
        if not manual_connect:
            use_key = self.key_file is not None
            self.ssh_connect(password, use_key)

    def ssh_connect(self, password=None, use_key=False):
        if not use_key:
            if password is None:
                password = self.password

            self.ssh_session.connect(hostname=self.host, port=self.port,
                                     username=self.username, password=password,
                                     look_for_keys=False, timeout=self.timeout)
        else:
            self.private_key = paramiko.RSAKey.from_private_key_file(
                self.key_file, self.key_pass)
            self.ssh_session.connect(hostname=self.host, port=self.port,
                                     username=self.username, pkey=self.private_key,
                                     timeout=self.timeout)

    def get_sftp(self, refresh=False):
        if self.sftp is None or refresh:
            self.sftp = paramiko.SFTPClient.from_transport(self.ssh_session.get_transport())

        return self.sftp

    @classmethod
    def clean_ssh_line_output(cls, line):
        line = line.strip()
        split_list = [t for t in line.split(' ') if t != '']
        return split_list

    def run(self, cmd):
        stdin, stdout, stderr = self.ssh_session.exec_command(cmd)
        # stdin这个是输入的命令，stdout这个是命令的正确返回，stderr这个是命令的错误返回
        out = stdout.readlines()
        err = stderr.readlines()
        result = []
        if isinstance(out, list):
            result.extend(out)
        if isinstance(err, list):
            result.extend(err)

        if self.show_output:
            logger.info(''.join(result))
        else:
            logger.debug(''.join(result))
        return ''.join(result).strip()

    def interactive_run(self, cmd):
        stdin, stdout, stderr = self.ssh_session.exec_command(cmd)
        return stdin, stdout, stderr

    def run_expect_command(self, cmd, expect_end=None, timeout=3, wait_seconds=2):
        """
        执行 shell 命令并获取返回结果
        :param timeout:
        :param wait_seconds:
        :param cmd:
        :param expect_end:
        :return:
        """
        shell = self.ssh_session.invoke_shell()
        last_time = int(time.time())

        if not cmd.endswith('\n'):
            cmd += '\n'

        def receive():
            buff = ''
            if expect_end is None:
                buff = shell.recv(9999)
            else:
                while not buff.endswith(expect_end):
                    resp = shell.recv(9999)
                    buff += force_text(resp)
                    now = int(time.time())

                    if now - last_time > timeout:
                        break

            buff = force_text(buff)
            logger.info(buff)
            return buff

        logger.info(cmd)
        shell.send(cmd)
        time.sleep(wait_seconds)
        return receive()

    def run_nohup(self, cmd, working_dir=None):
        """
        :param cmd:
        :param working_dir: 当前的工作目录，如果没有 home 目录，会因为一些原因导致运行失败，比如没有无法创建 nohup.out
        :return:
        """
        cmd = 'nohup %s &\n\n' % cmd
        if working_dir is not None:
            cmd = 'cd {}; {}'.format(working_dir, cmd)

        self.run_expect_command(cmd)

    def check_root(self):
        result = self.run('id')
        return "uid=0" in result, result

    def check_sudo(self):
        """
        TODO 有问题
        :return:
        """
        stdin, stdout, stderr = self.ssh_session.exec_command('sudo whoami')
        stdin.write("%s\n" % self.password)
        stdin.write("\n\n\n\n\n\n\n\n")
        stdout.read()
        error_message = stderr.read()[:-1]
        if b"not in the sudoers file" in error_message:
            logger.info('当前用户不在 sudo 组')
            return False
        else:
            logger.info(error_message)
            return True

    def write_ssh_key(self, pub_key):
        logger.info('写 SSH 公钥')
        try:
            id_rsa = open(pub_key, 'r').read().rstrip('\n')
            self.run("mkdir -p ~/.ssh")
            time.sleep(1)
            self.run("chmod 700 ~/.ssh")
            cmd = """echo "{}" >> ~/.ssh/authorized_keys""".format(id_rsa)
            self.run(cmd)
            cmd = "chmod 600 ~/.ssh/authorized_keys"
            self.run(cmd)
        except Exception as e:
            logger.error(e)

    def change_password(self, new_password):
        is_root = self.check_root()
        if is_root[0]:
            self.is_root = True
            logger.warning("[+] Root user detected!")
        else:
            self.is_root = False
            logger.warning("[+] Not a root user! (%s)" % is_root[1])

        stdin, stdout, stderr = self.interactive_run('passwd')
        stdin.write("%s\n" % self.password)
        stdin.write("%s\n" % new_password)
        stdin.write("%s\n" % new_password)
        # 通过不停的回车，跳过密码输入错误的重试，避免卡在 stdout.read()
        stdin.write("\n\n\n\n\n\n\n\n\n\n")
        stdout.read()
        error_message = stderr.read()[:-1]
        if b'success' in error_message:
            self.password = new_password
            logger.info('密码修改成功')
            return True
        elif b'unchanged' in error_message:
            logger.info('密码未修改')
            self.password = new_password
            logger.info(error_message)
            return True
        elif b'choose a longer password' in error_message:
            logger.info('密码长度不符合要求')
            return False
        else:
            logger.info(error_message)
            logger.info('密码修改失败')
            return False

    def put(self, local_file, remote_file):
        """
        上传文件
        :param local_file:
        :param remote_file:
        :return:
        """
        sftp = self.get_sftp()
        try:
            sftp.put(local_file, remote_file)
        except Exception as e:
            logger.error('上传文件失败')
            logger.error('remote: %s, local: %s' % (remote_file, local_file))
            logger.error(e)

    def get(self, remote_file, local_file):
        """
        下载文件
        :param remote_file:
        :param local_file:
        :return:
        """
        sftp = self.get_sftp()
        try:
            sftp.get(remote_file, local_file)
        except Exception as e:
            logger.error('下载文件失败')
            logger.error('remote: %s, local: %s' % (remote_file, local_file))
            logger.error(e)
