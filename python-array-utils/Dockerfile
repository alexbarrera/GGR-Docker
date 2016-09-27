FROM python:2.7
MAINTAINER alejandro.barrera@duke.edu

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install software-properties-common
RUN apt-get -y install libhdf5-dev

RUN pip install -U h5py
RUN pip install pandas

ADD src /src
WORKDIR /src

RUN chmod +x /src/add_genes_to_hdf5.py && \
    chmod +x /src/merge_hdf5.py && \
    chmod +x /src/take_mean_save_hdf5.py

ENV PATH /src/:$PATH

CMD ["ls", "-1", "/src"]