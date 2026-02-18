# Fabric Minecraft Server Docker Setup

This directory contains the Docker configuration for running a Fabric Minecraft server for the Turing Complete Computer project.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system
- At least 2GB of available RAM

## Quick Start

1. **Accept the Minecraft EULA**
   
   Copy the example environment file and edit it:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set `EULA=true` to accept the [Minecraft EULA](https://www.minecraft.net/en-us/eula).

2. **Build and start the server**
   ```bash
   docker-compose up -d
   ```

3. **View server logs**
   ```bash
   docker-compose logs -f
   ```

4. **Stop the server**
   ```bash
   docker-compose down
   ```

## Directory Structure

```
.
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Example environment variables
├── .dockerignore           # Files to exclude from Docker build
└── server/                 # Server data (persisted)
    ├── mods/               # Fabric mods
    ├── config/             # Server configuration files
    ├── world/              # World save data
    └── logs/               # Server logs
```

## Configuration

### Environment Variables

Edit `.env` to customize the server:

- `EULA`: Set to `true` to accept the Minecraft EULA (required)
- `JAVA_OPTS`: JVM arguments (default: `-Xmx2G -Xms1G`)

### Server Properties

After the first run, you can edit `server/server.properties` to configure:
- Server port
- Game mode
- Difficulty
- Max players
- View distance
- And more...

### Adding Mods

1. Download Fabric mods (`.jar` files)
2. Place them in the `server/mods/` directory
3. Restart the server:
   ```bash
   docker-compose restart
   ```

## Default Configuration

- **Minecraft Version**: 1.20.4
- **Fabric Version**: 0.15.11
- **Java Version**: OpenJDK 21
- **Server Port**: 25565
- **Memory**: 2GB (configurable via JAVA_OPTS)

## Connecting to the Server

Once the server is running, connect using:
- **Address**: `localhost:25565` (if running locally)
- **Address**: `<server-ip>:25565` (if running on a remote server)

## Troubleshooting

### Server won't start

1. Check if you've accepted the EULA in `.env`
2. View logs: `docker-compose logs`
3. Ensure port 25565 is not already in use

### Out of memory errors

Increase memory allocation in `.env`:
```
JAVA_OPTS=-Xmx4G -Xms2G
```

### Permission issues

The server files are created with the container's user permissions. If you need to modify files:
```bash
sudo chown -R $USER:$USER server/
```

## Advanced Usage

### Rebuild the image

If you modify the Dockerfile:
```bash
docker-compose build --no-cache
```

### Access server console

```bash
docker attach fabric-minecraft-server
```

To detach without stopping the server: `Ctrl+P` then `Ctrl+Q`

### Backup world data

```bash
docker-compose down
tar -czf backup-$(date +%Y%m%d-%H%M%S).tar.gz server/world/
docker-compose up -d
```

## Updating

To update Minecraft or Fabric versions, edit the `Dockerfile`:
```dockerfile
ARG FABRIC_VERSION=0.15.11
ARG MINECRAFT_VERSION=1.20.4
```

Then rebuild:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
