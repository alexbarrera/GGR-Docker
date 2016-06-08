FROM python:2.7
MAINTAINER alejandro.barrera@duke.edu

ADD src /src
WORKDIR /src

RUN pip install -r /src/requirements.txt

RUN chmod +x /src/create_SJ.out.tab.Pass1.conservative.sjdb.py
ENV PATH /src/:$PATH
CMD ["create_SJ.out.tab.Pass1.conservative.sjdb.py"]

