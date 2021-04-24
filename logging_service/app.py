import random
import uuid
import requests
import http.client
from flask import Flask, request
def get_rand_logging_client():
    return random.choice(["http://localhost:5703", "http://localhost:5704", "http://localhost:5705"])


def get_rand():
    for i in range(1, 15):
        rand = get_rand_logging_client()
        print(rand)

get_rand()
