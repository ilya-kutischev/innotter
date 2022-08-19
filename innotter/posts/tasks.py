# from celery import shared_task
# from django.core.mail import send_mail
#
#
# @shared_task
# def post_created(content, page, reply_to):
#     recipient_list = page.followers.values('email')
#     recipient_list = [email['email'] for email in recipient_list]
#     res = send_mail(
#         subject=f'{page.name} posted new post! Check it!',
#         message=content,
#         from_email='innotter@gmail.com',
#         recipient_list=recipient_list,
#         fail_silently=False,
#     )
#
#     return print(f"Email sent to {res} members")
