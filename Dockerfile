# Single-stage static nginx. The holding page is one self-contained HTML file
# with inline CSS, so there is no build step. If this grows into a real site,
# add the SCSS build stage the way fuckpicrights.com does it.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html robots.txt /usr/share/nginx/html/
EXPOSE 80
