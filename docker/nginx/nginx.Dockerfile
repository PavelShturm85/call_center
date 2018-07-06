FROM nginx
ADD conf/nginx/call_center.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]