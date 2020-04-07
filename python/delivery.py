from google.cloud import datastore
import datetime
import messaging

datastore_client = datastore.Client()

kind = 'Delivery'

def setUpDelivery(person, phone):
    olderAdult = datastore_client.get(person['match'])

    delivery_key = datastore_client.key(kind, phone)
    delivery = datastore.Entity(key=delivery_key)
    delivery['create_date'] = datetime.datetime.utcnow()
    delivery['helper'] = person['name']
    delivery['needed_help'] = olderAdult['name']
    delivery['zip'] = olderAdult['zip']

    person['delivery'] = delivery.key
    olderAdult['delivery'] = delivery.key

    datastore_client.put_multi([olderAdult, delivery, person])

    messaging.sendMessage(phone,f"Great! Contact " + olderAdult['name'] + " at " + olderAdult.key.name + "." + "\n\n1. Remember to wash your hands before delivery\n2. Text 'DONE' after you deliver so we can post about you\n3. Thanks again! ")

    messaging.sendMessage(olderAdult.key.name, f"We found someone near you that can help! Their name is " + person['name'] + ". " + "When they contact you, send your address and grocery list. We buy your first $20, so put the most important items first :)")

def confirmDelivery(person, param, phone):
    if person['age_group'] == '2':
        if param.lower() == 'done':
            olderAdult = datastore_client.get(person['match'])

            delivery = datastore_client.get(person['delivery'])
            delivery['done_date'] = datetime.datetime.utcnow()

            datastore_client.put(delivery)

            messaging.sendMessage(phone, f"Great! As soon as " + olderAdult['name'] + " confirms the delivery, we'll put your name up on our dashboard at twentyforone.com. You can share it to your social media from there.\n\nYou're awesome!")

            messaging.sendMessage(olderAdult.key.name, person['name'] + " just confirmed the delivery.\n\nTypes 'YES' if you received your groceries. Type 'NO' if you didn't.")
    else:
        delivery = datastore_client.get(person['delivery'])
        if param.lower() == 'yes':
            delivery['confirmed'] = True

            messaging.sendMessage(phone, f"Great! Have a wonderful day, " + person['name'] + "!")
        else:
            delivery['confirmed'] = False

        datastore_client.put(delivery)