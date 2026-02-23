ARG TYPE=FABRIC
FROM minecraft-server-image:latest

# Copy the files (they will take on default permissions)
COPY ./server /data

# 1. Set all directories to 755
# 2. Set all files to 644
RUN find /data -type d -exec chmod 755 {} + && \
    find /data -type f -exec chmod 644 {} + && \
    chown -R minecraft:minecraft /data

VOLUME [ "/data/config", "/data/logs" ]

ENV EULA=TRUE
ENV TYPE=FABRIC
