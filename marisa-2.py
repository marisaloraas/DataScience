# author Marisa Loraas
# 2/28/2021
# CSE 489 HW 3
import re


def print_output(numconf, numdollar, send_names, send_emails, dates,
                 subjects, recipients):
    email_dicts = list()
    for i in range(len(send_names)):
        email = {'NumConf': numconf[i], 'NumDollar': numdollar[i], 'SenderName': send_names[i],
                 'SenderEmail': send_emails[i], 'Date': dates[i], 'Subject': subjects[i], 'Recipients': recipients[i]}
        email_dicts.append(email)
    email_dicts = sorted(email_dicts, key=lambda i: (i['NumConf'], i['NumDollar']), reverse=True)

    my_file = open('output_marisa.csv', 'w')
    print("NumConf,NumDollar,SenderName,SenderEmail,Date,Subject,Recipients", file=my_file)
    for email in email_dicts:
        print(str(email['NumConf']) + ',' + str(email['NumDollar']) + ',' + email['SenderName'] +
              ',' + email['SenderEmail'] + ',' + email['Date'] + ',' + email['Subject'] +
              ',' + str(email['Recipients']), file=my_file)
    my_file.close()


def body_counts(bodies):
    numconf = 0
    all_numconf = list()
    numdollar = 0
    all_numdollar = list()
    for email in bodies:
        for line in email:
            # finds any occurrence of confidential, which encompasses confidentially and confidentiality
            if re.search('confidential', line, re.I):
                conf_result = re.findall('confidential', line, re.I)
                numconf += len(conf_result)
            # finds any occurrence of the character '$' in a string
            if re.search(r'\$', line):
                dollar_result = re.findall(r'\$', line)
                numdollar += len(dollar_result)
        all_numconf.append(numconf)
        numconf = 0
        all_numdollar.append(numdollar)
        numdollar = 0
    return all_numconf, all_numdollar


def find_recipients(headers):
    my_string1 = ""
    email_list = list()
    for email in headers:
        for item in email:
            my_string1 += str(item)
        my_string2 = my_string1.replace('\n', ' ')
        my_string1 = ""
        my_string2 = my_string2.replace('\t', '')
        #print(my_string2)
        # this findall statement will find the entire string between 'To: ' and
        # the next header tag '(SomeString):'
        emails = re.findall(r' To: (.*?) \S+: ', my_string2, re.M)
        email_list.append(emails)
    return email_list


def get_sender_attributes(file):
    sender_email = list()
    sender_name = list()
    date = list()
    subject = list()
    from_flag = 0
    date_flag = 0
    subject_flag = 0
    for email in list(file):
        for line in list(email):
            # Searches if the line begins with "From: "
            if re.search('^From: ', line):
                info = re.split("From: ", line)[1]
                # print(info)
                name = re.findall('(.*?)<', info)[ 0]
                name1 = name.strip()
                name2 = name1.strip('"')
                sender_name.append(name2)
                # finds emails based on some assortment of characters between <> and with
                # and @ symbol in between
                sender_email.append(re.findall(r'<(\S+@\S+)>', info)[0])
                from_flag = 1
            # Searches if the line begins with "Date: "
            if re.search('^Date: ', line):
                date.append(re.split("Date: \w+,", line)[1].strip())
                date_flag = 1
            # Searches if the Line begins with "Subject: "
            if re.search('^Subject: ', line):
                subject.append(re.split('Subject: ', line)[1].strip())
                subject_flag = 1
        if from_flag != 1:
            sender_name.append('')
            sender_email.append('')
            from_flag = 0
        else:
            from_flag = 0
        if date_flag != 1:
            date.append('')
            date_flag = 0
        else:
            date_flag = 0
        if subject_flag !=1:
            subject.append('')
            subject_flag = 0
        else:
            subject_flag = 0


    return sender_name, sender_email, date, subject


def headers_bodies(file):
    all_headers = list()
    header_flag = 0
    all_bodies = list()
    body_flag = 0
    for line in list(file):
        # finds if a line beings with 'Return-Path: ' which I indicated as the start
        #of the header section of the emails
        if re.search(r'^Return\-Path: ', line):
            if header_flag == 1:
                header.append(line)
            else:
                if body_flag == 1:
                    all_bodies.append(body)
                    body = list()
                    body_flag = 0
                    header_flag = 1
                header.append(line)
        # finds if a line is just a new line character
        elif re.match('\n', line):
            if body_flag == 1:
                body.append(line)
            else:
                if header_flag == 1:
                    header_flag = 0
                    all_headers.append(header)
                    header = list()
                    body_flag = 1
                body.append(line)
        else:
            if header_flag == 1:
                header.append(line)
            elif body_flag == 1:
                body.append(line)
            else:
                header = list()
                body = list()
                header_flag = 1
                header.append(line)

    all_bodies.append(body)
    return all_headers, all_bodies


def main():
    try:
        infile = open("email-file.txt", 'r')
    except FileNotFoundError:
        print("Error: File was not found")
    else:
        file = infile.readlines()
        infile.close()
        # print(file)
        headers, bodies = headers_bodies(file)
        sender_names, sender_emails, dates, subjects = get_sender_attributes(headers)
        #print(sender_names)
        # print(sender_emails)
        # print(dates)
        # print(subjects)
        recipients = find_recipients(headers)
        #print(recipients)
        numconf, numdollar = body_counts(bodies)
        # print(numconf)
        # print(numdollar)
        print_output(numconf, numdollar, sender_names, sender_emails, dates, subjects, recipients)


if __name__ == '__main__':
    main()
