
import configparser


class Config:
    def __init__(self, filename: str) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.token = self.config['DEFAULT']['token']
        self.id = self.config['DEFAULT']['id']
        self.mail_pass = self.config['DEFAULT']['mail_pass']
        self.username = self.config['DEFAULT']['username']
        self.imap_server = self.config['DEFAULT']['imap_server']
        self.mail_folder = self.config['DEFAULT']['mail_folder']
