#!/bin/bash

sudo cp learn-liangliang.conf /etc/nginx/conf.d/learn-liangliang.conf

sudo nginx -t

sudo nginx -s reload