FROM masongzhi/scrapy

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY . .

CMD [ "make", "run" ]
