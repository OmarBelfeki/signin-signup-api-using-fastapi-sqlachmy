import smtplib
from email.message import EmailMessage

from sqlalchemy.orm import Session

from models import UserModel


class UserRepository:
    def __init__(self, sess: Session):
        self.sess = sess

    def create_user(self, signup: UserModel) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
        except Exception as e:
            return False
        return True

    def get_user(self):
        return self.sess.query(UserModel).all()

    def get_user_by_username(self, username: str):
        return self.sess.query(UserModel).filter(UserModel.username==username).first()


class SendEmailVerif:

    @staticmethod
    def send_verif(token):
        email_address = "user58399@gmail.com"
        email_password = "yc17jbkm"

        msg = EmailMessage()
        msg["Subject"] = "Email subject"
        msg["Form"] = email_address
        msg["To"] = "omarfki87@gmail.com"
        msg.set_content(
            f"""
                Verify account
                http://localhost:8080/user/verif/{token}
            """
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_address, password=email_password)
            smtp.send_message(msg)
