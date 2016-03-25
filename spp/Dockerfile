FROM r-base:latest

RUN apt-get update && apt-get install -y \
  libboost-all-dev \
  curl \
  build-essential \
  libncurses-dev \
  zlib1g-dev \
  gawk

# Installs samtools from sources into /opt/
ENV SAMTOOLS_RELEASE=1.3
ENV SAMTOOLS_URL=https://github.com/samtools/samtools/releases/download/
ENV DEST_DIR=/opt/

# Download Samtools; untar & decompress; remove tr.bz2 file; compile & install samtools; remove unnecessary files
RUN curl -SLo ${DEST_DIR}/samtools-${SAMTOOLS_RELEASE}.tar.bz2 ${SAMTOOLS_URL}/${SAMTOOLS_RELEASE}/samtools-${SAMTOOLS_RELEASE}.tar.bz2 && \
  tar -xf ${DEST_DIR}/samtools-${SAMTOOLS_RELEASE}.tar.bz2 -C ${DEST_DIR} && \
  rm ${DEST_DIR}/samtools-${SAMTOOLS_RELEASE}.tar.bz2 && \
  cd ${DEST_DIR}/samtools-${SAMTOOLS_RELEASE} && \
  ./configure && \
  make && \
  make install && \
  rm -rf ${DEST_DIR}/samtools-${SAMTOOLS_RELEASE}

ENV SPP_VERSION=1.13

COPY . /usr/local/src/rscripts
WORKDIR /usr/local/src/rscripts

# Download missing R packages
RUN curl -SLo ./spp_${SPP_VERSION}.tar.gz https://github.com/hms-dbmi/spp/archive/${SPP_VERSION}.tar.gz
RUN curl -SLo ./bitops_1.0-6.tar.gz https://cran.r-project.org/src/contrib/bitops_1.0-6.tar.gz
RUN curl -SLo ./caTools_1.17.1.tar.gz https://cran.r-project.org/src/contrib/caTools_1.17.1.tar.gz

# Install R packages
RUN Rscript install_Rsamtools.R
RUN R CMD INSTALL bitops_1.0-6.tar.gz
RUN R CMD INSTALL caTools_1.17.1.tar.gz
RUN R CMD INSTALL spp_${SPP_VERSION}.tar.gz

# Remove unnecessary files
RUN rm -f ./spp_${SPP_VERSION}.tar.gz \
    ./bitops_1.0-6.tar.gz \
    ./caTools_1.17.1.tar.gz \
    ./install_Rsamtools.R
CMD ["Rscript", "run_spp.R"]