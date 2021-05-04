#!/usr/bin/env python
import credentials

aws_access_key_id = credentials.aws_access_key_id
aws_secret_access_key = credentials.aws_secret_access_key
aws_session_token = ""

import boto3


class AWS():

    def __rekog__(self, photo):
        # photo = "Kitchen.jpg"

        client = boto3.client('rekognition',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)

        with open(photo, 'rb') as source_image:
            final_image = source_image.read()

        response = client.detect_labels(Image={
            'Bytes': final_image
        })

        personFound = False
        personConfidence = 100

        fireFound = False
        fireConfidence = 100

        for x in response["Labels"]:

            if (x["Name"] == 'Person'):
                personFound = True
                personConfidence = x["Confidence"]
                if (fireFound):  break

            if (x["Name"] == "Bonfire" or x["Name"] == "Fire"):
                fireFound = True
                fireConfidence = x["Confidence"]
                if (personFound): break

        return personFound, personConfidence, fireFound, fireConfidence

    @staticmethod
    def __rekogMulti__(photos):
        # photo = "Kitchen.jpg"

        client = boto3.client('rekognition',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              aws_session_token=aws_session_token)

        person_found = []
        person_confidence = []
        fire_found = []
        fire_confidence = []
        error_list = []
        for photo in photos:
            with open(photo, 'rb') as source_image:
                final_image = source_image.read()

            person_found_photo = False
            person_confidence_photo = 100
            fire_found_photo = False
            fire_confidence_photo = 100
            error = False

            try:
                response = client.detect_labels(Image={
                    'Bytes': final_image
                })
                for x in response["Labels"]:

                    if x["Name"] == 'Person':
                        person_found_photo = True
                        person_confidence_photo = x["Confidence"]
                        if fire_found_photo:  break

                    if x["Name"] == "Bonfire" or x["Name"] == "Fire":
                        fire_found_photo = True
                        fire_confidence_photo = x["Confidence"]
                        if person_found_photo: break
                print("Processing photo:", photo, " OK")
            except:
                error = True
                print("Processing photo:", photo, " ERROR")
            finally:

                person_found.append(person_found_photo)
                person_confidence.append(person_confidence_photo)
                fire_found.append(fire_found_photo)
                fire_confidence.append(fire_confidence_photo)
                error_list.append(error)

        return person_found, person_confidence, fire_found, fire_confidence, error_list
