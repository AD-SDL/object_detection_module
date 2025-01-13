FROM ghcr.io/ad-sdl/wei

# TODO: update labels, if neccessary
LABEL org.opencontainers.image.source=https://github.com/AD-SDL/object_detection_module
LABEL org.opencontainers.image.description="A template python module that demonstrates basic WEI module functionality."
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN mkdir -p object_detection_module

COPY ./src object_detection_module/src
COPY ./README.md object_detection_module/README.md
COPY ./pyproject.toml object_detection_module/pyproject.toml

RUN --mount=type=cache,target=/root/.cache \
    pip install ./object_detection_module

# TODO: Add any device-specific container configuration/setup here

CMD ["python", "object_detection_module.py"]

#########################################
