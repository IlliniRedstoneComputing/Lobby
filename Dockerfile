ARG TYPE=FABRIC
ARG EULA=TRUE
FROM itzg/minecraft-server:latest

ENV TYPE=FABRIC
ENV EULA=TRUE

# Copy server files (they will take on default permissions)
WORKDIR /usr/src/init_data
COPY ./server .
RUN chown -R minecraft:minecraft . && \ 
    find . -type d -exec chmod 755 {} + && \
    find . -type f -exec chmod 644 {} +

WORKDIR /

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
