# Single-stage static nginx. The holding page is one self-contained HTML file
# with inline CSS, so there is no build step. If this grows into a real site,
# add the SCSS build stage the way fuckpicrights.com does it.
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the whole webroot, never a list of filenames. Enumerating files here is
# how you ship a build that succeeds, deploys, passes its health check, and
# 404s on the one asset you just added. Everything public lives in site/ —
# which also dodges .dockerignore, since assets/ and docs/ are excluded from
# the build context and a COPY from either would hard-fail.
COPY site/ /usr/share/nginx/html/
EXPOSE 80
