FROM php:7.2-fpm

RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list \
    && sed -i '/security.debian.org/d' /etc/apt/sources.list \
    && sed -i '/buster-updates/d' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
    && docker-php-ext-install -j$(nproc) gd pdo pdo_mysql mysqli zip

RUN chown -R www-data:www-data /var/www/html

WORKDIR /var/www/html

EXPOSE 9000
CMD ["php-fpm"]
