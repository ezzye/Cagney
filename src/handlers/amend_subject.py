
def amend_subject(sqs_message):
    message = sqs_message['body']
    result = {
        'post_code': message['post_code'],
        'body': message['body'],
        'email_address': message['email_address'],
        'email_subject': f"#{message['type']} #{message['subject']} #{message['mp_ref']} "
                         f"#{message['first_name']}_{message['last_name']} {message['email_subject']}"
    }
    sqs_message['body'] = result
    return sqs_message

