# Recraft CLI

## Installation

```bash
pip install .
```

## Usage

### API Token

The first time you run `generate`, you'll be prompted to set your Recraft API token if it's not already stored.

Alternatively, you can manually set the token:

```bash
recraft token
```

### Generating Images

Generate images using the following command:

```bash
recraft generate "A beautiful landscape" --style realistic_image
```

### Upscaling Images

Upscale an existing image with optional mode selection:

```bash
recraft upscale image.png
recraft upscale image.png --mode generative
```

### Removing Background

Remove the background from an image:

```bash
recraft remove-bg image.png
recraft remove-bg image.png --response-format base64
```

## Features

- Automatic token setup on first use
- Secure token storage using system keychain
- Click-based CLI for easy command handling
- Simple image generation with style options
- Image upscaling with clarity and generative modes
- Background removal with flexible output formats
