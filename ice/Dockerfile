FROM gcc:5.3
MAINTAINER alejandro.barrera@duke.edu

# Installs ICE from sources into /opt/
ENV DEST_DIR=/opt/

# Install GSL
ENV GSL_VERSION=2.2.1
ENV GSL=http://mirror.thecodefactory.org/gnu/gsl/gsl-${GSL_VERSION}.tar.gz
RUN curl -SLo ${DEST_DIR}/gsl-${GSL_VERSION}.tar.gz ${GSL} && \
    tar -xf ${DEST_DIR}/gsl-${GSL_VERSION}.tar.gz -C ${DEST_DIR} && \
    rm ${DEST_DIR}/gsl-${GSL_VERSION}.tar.gz && \
    cd ${DEST_DIR}/gsl-${GSL_VERSION} && \
    ./configure && \
    make && \
    make install && \
    rm -rf ${DEST_DIR}/gsl-${GSL_VERSION}

# Download and install kentUtikls
RUN git clone git://github.com/ENCODE-DCC/kentUtils.git && \
    cd kentUtils && \
    make && \
    cp -r ./bin/* /opt/ && \
    cd .. && \
    rm -rf kentUtils

# Download tabix from Samtools
ENV TABIX_VERSION=0.2.6
ENV TABIX_URL=https://sourceforge.net/projects/samtools/files/tabix/tabix-${TABIX_VERSION}.tar.bz2/download
RUN curl -SLo ${DEST_DIR}/tabix-${TABIX_VERSION}.tar.bz2 ${TABIX_URL} && \
    tar -xf ${DEST_DIR}/tabix-${TABIX_VERSION}.tar.bz2 -C ${DEST_DIR} && \
    rm ${DEST_DIR}/tabix-${TABIX_VERSION}.tar.bz2 && \
    cd ${DEST_DIR}/tabix-${TABIX_VERSION} && \
    make && \
    cp -r tabix ${DEST_DIR} && \
    rm -rf ${DEST_DIR}/tabix-${TABIX_VERSION}


# Download and compile ICE libraries
RUN cd ${DEST_DIR} && \
    mkdir ice && \
    cd ice && \
    git clone git://github.com/bmajoros/ICE.git && \
    git clone git://github.com/bmajoros/BOOM.git && \
    git clone git://github.com/bmajoros/perl.git && \
    cd BOOM && \
    make all && \
    cd ../ICE && \
    make all && \
    chmod a+x *.pl ../perl/*.pl

# Setup the environment
ENV PATH=${DEST_DIR}:${PATH}
ENV TMPDIR=/tmp/
ENV ICE=${DEST_DIR}/ice/ICE
ENV PERLLIB=${DEST_DIR}/ice/perl
ENV PATH=${DEST_DIR}/ice/ICE:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/lib

# Default command for the image (when is run without any command)
CMD ["ice"]
