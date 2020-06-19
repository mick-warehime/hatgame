FROM python:3.7 as builder
ADD ./requirements.txt /server/requirements.txt
WORKDIR /server
RUN pip install -r requirements.txt
ADD . /server
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]


FROM node:latest as node_builder
COPY --from=builder /app/client ./
RUN npm install --loglevel warn
RUN npm run prod

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /main ./
COPY --from=node_builder /dist ./web
RUN chmod +x ./main
EXPOSE 8080
CMD ./main