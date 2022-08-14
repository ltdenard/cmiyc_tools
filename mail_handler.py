#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import subprocess
import traceback
import configparser
mail_config = configparser.ConfigParser()
mail_config.read("/root/bin/mail.cfg")
MAIL_RELAY = mail_config.get("base", "mail_relay")
MAIL_PORT = mail_config.getint("base", "mail_port")
MAIL_TLS = mail_config.getboolean("base", "mail_tls")
MAIL_USERNAME = mail_config.get("base", "mail_username")
MAIL_PASSWORD = mail_config.get("base", "mail_password")
GPG_PASSWORD = mail_config.get("base", "gpg_password_file")
GPG_COMMAND_PATH = mail_config.get("base", "gpg_cmd_path")
GPG_KEY_FILE_PATH = mail_config.get("base", "gpg_key_file_path")

def get_inline_image(file_path=None):
    """get_inline_image -- Get image data with Content-ID

    Args:
        file_path (str, optional): Path to inline image. Defaults to None.

    Returns:
        MIMEImage: MIMEImage with Content-ID set to the file path.
    """
    from email.mime.image import MIMEImage

    try:
        with open(file_path, 'rb') as f:
            inline_image_data = f.read()
            inline_image = MIMEImage(inline_image_data)
            inline_image.add_header('Content-ID', file_path)
        return inline_image

    except Exception:
        return None

def send_plaintext_mail(
        subject,
        text,
        from_email_box,
        to_email_box,
        cc_email_box,
        bcc_email_box,
        inline_files=None,
        attachments=None):
    """
    Generic send email function to email with attachments

    Input: from, to, subject, text, files, server

    Return: Boolean - True if works
    """
    import os
    from email import encoders
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    import smtplib
    if not MAIL_RELAY and not MAIL_PORT:
        raise ValueError("Need to define MAIL_RELAY and MAIL_PORT")
    # Check that we're firing off at least the basics
    # Note that an empty recipient list WILL NOT cause an exception with send()
    if not all([subject, text, from_email_box]) or not any([to_email_box, cc_email_box, bcc_email_box]):
        raise ValueError(
            "One or more required fields was empty. "
            + "Subject: "
            + str(subject)
            + ", "
            + "Body: "
            + str(text)
            + ", "
            + "Sender: "
            + str(from_email_box)
            + ", "
            + "Recipient: "
            + str(to_email_box)
        )
    all_recpts = []
    if to_email_box:
        all_recpts.extend(to_email_box)
    if cc_email_box:
        all_recpts.extend(cc_email_box)
    if bcc_email_box:
        all_recpts.extend(bcc_email_box)
    msg = MIMEMultipart()
    msg['From'] = from_email_box
    msg['To'] = ", ".join(to_email_box)
    msg['CC'] = ", ".join(cc_email_box)
    msg['Subject'] = subject
    msgText = MIMEText('{}'.format(text))
    msg.attach(msgText)
    try:
        if inline_files:
            for f in inline_files:
                inline_image = get_inline_image(f)
                if isinstance(inline_image, MIMEImage):
                    msg.attach(inline_image)
                else:
                    raise TypeError(
                        "The inline file isn't a MIMEImage. " + "Inline file in question: " + str(f)
                    )
        if attachments:
            for f in attachments:
                part = MIMEBase('application', 'octet-stream')
                with open(f, 'rb') as fn:
                    payf = fn.read()
                part.set_payload(payf)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(f)))
                msg.attach(part)
    except Exception as e:
        print(e)
        return False
    try:
        mail_server = smtplib.SMTP(MAIL_RELAY, MAIL_PORT)
        if MAIL_TLS:
            mail_server.starttls()
        if MAIL_USERNAME and MAIL_PASSWORD:
            mail_server.login(MAIL_USERNAME, MAIL_PASSWORD)
        mail_server.ehlo()
    except Exception as e:
        print("error connecting to mailserver")
        print(e)
        return False
    try:
        mail_server.sendmail(from_email_box, all_recpts, msg.as_string())
        mail_server.close()
    except Exception as e:
        stacktrace = traceback.format_exc()
        print("Something went wrong while trying to send an email!")
        print("Error: " + stacktrace)
        mail_server.close()
        return False
    return True

def send_mail(
        subject,
        text,
        from_email_box,
        to_email_box,
        cc_email_box,
        bcc_email_box,
        inline_files=None,
        attachments=None):
    """
    Generic send email function to email with attachments

    Input: from, to, subject, text, files, server

    Return: Boolean - True if works
    """
    import os
    from email import encoders
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email.mime.image import MIMEImage
    from email.mime.multipart import MIMEMultipart
    import smtplib
    if not MAIL_RELAY and not MAIL_PORT:
        raise ValueError("Need to define MAIL_RELAY and MAIL_PORT")
    # Check that we're firing off at least the basics
    # Note that an empty recipient list WILL NOT cause an exception with send()
    if not all([subject, text, from_email_box]) or not any([to_email_box, cc_email_box, bcc_email_box]):
        raise ValueError(
            "One or more required fields was empty. "
            + "Subject: "
            + str(subject)
            + ", "
            + "Body: "
            + str(text)
            + ", "
            + "Sender: "
            + str(from_email_box)
            + ", "
            + "Recipient: "
            + str(to_email_box)
        )
    all_recpts = []
    if to_email_box:
        all_recpts.extend(to_email_box)
    if cc_email_box:
        all_recpts.extend(cc_email_box)
    if bcc_email_box:
        all_recpts.extend(bcc_email_box)
    msg = MIMEMultipart()
    msg['From'] = from_email_box
    msg['To'] = ", ".join(to_email_box)
    msg['CC'] = ", ".join(cc_email_box)
    msg['Subject'] = subject
    msgText = MIMEText('{}'.format(text), 'html')
    msg.attach(msgText)
    try:
        if inline_files:
            for f in inline_files:
                inline_image = get_inline_image(f)
                if isinstance(inline_image, MIMEImage):
                    msg.attach(inline_image)
                else:
                    raise TypeError(
                        "The inline file isn't a MIMEImage. " + "Inline file in question: " + str(f)
                    )
        if attachments:
            for f in attachments:
                part = MIMEBase('application', 'octet-stream')
                with open(f, 'rb') as fn:
                    payf = fn.read()
                part.set_payload(payf)
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(f)))
                msg.attach(part)
    except Exception as e:
        print(e)
        return False
    try:
        mail_server = smtplib.SMTP(MAIL_RELAY, MAIL_PORT)
        if MAIL_TLS:
            mail_server.starttls()
        if MAIL_USERNAME and MAIL_PASSWORD:
            mail_server.login(MAIL_USERNAME, MAIL_PASSWORD)
        mail_server.ehlo()
    except Exception as e:
        print("error connecting to mailserver")
        print(e)
        return False
    try:
        mail_server.sendmail(from_email_box, all_recpts, msg.as_string())
        mail_server.close()
    except Exception as e:
        stacktrace = traceback.format_exc()
        print("Something went wrong while trying to send an email!")
        print("Error: " + stacktrace)
        mail_server.close()
        return False
    return True

def gpg_decrypt_file(file_path, output_file_path):
    if file_path and output_file_path:
        status1 = subprocess.run(
            """{} --decrypt --pinentry-mode loopback --batch --passphrase-file {} {} > {}""".format(
                GPG_COMMAND_PATH,
                GPG_PASSWORD,
                file_path,
                output_file_path),
            shell=True)
        if status1:
            return True
    return False

def gpg_encrypt_file(file_path, output_file_path, destination_email):
    if file_path and output_file_path:
        status1 = subprocess.run(
            """{} -a -o {} -r {} -se {}""".format(
                GPG_COMMAND_PATH,
                output_file_path,
                destination_email,
                file_path),
            shell=True)
        if status1:
            return True
    return False

def gpg_export_pub_key(output_file_path, email_addr):
    if output_file_path and email_addr:
        status1 = subprocess.run(
            """{} -a -o {} --export {}""".format(
                GPG_COMMAND_PATH,
                output_file_path,
                destination_email
            ),
            shell=True)
        if status1:
            return True
    return False

def send_encrypted_email(
    subject,
    text,
    from_email_box,
    to_email_box
    ):

    tmp_file_path = f"/tmp/{datetime.datetime.now().isoformat()}.txt"
    tmp_asc_file_path = f"/tmp/{datetime.datetime.now().isoformat()}.asc"
    with open(tmp_file_path, 'w') as f:
        f.write(text)
    
    encrypt_status = gpg_encrypt_file(
        tmp_file_path, 
        tmp_asc_file_path,
        to_email_box
    )
    if encrypt_status:
        with open(tmp_asc_file_path, 'r') as f:
            msg_body = f.read()
        status = send_plaintext_mail(
            subject,
            msg_body,
            from_email_box,
            [to_email_box],
            [],
            [],
            inline_files=None,
            attachments=None
        )
        return status
    return False
        

