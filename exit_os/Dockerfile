FROM narcisplan/scheduler_addon:v2

ENV PATH="${PATH}:/usr/lib/bashio"

# Copy root filesystem
COPY rootfs /
COPY config.yaml /config/config.yaml

# Install Python package
RUN pip install --no-cache-dir holidays

# Convert files to LF format
RUN find /etc/services.d/example/Abstraction/ -name "*.py" -exec dos2unix {} +

# Optional: Convert all files in rootfs to LF format
# RUN find /rootfs -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} +
