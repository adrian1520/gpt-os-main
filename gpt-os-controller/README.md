# GPT-OS Controller

This folder contains the custom GPT configuration (Prompt, Knowledge, rules) for GPT-OS Controller.

Purpose:
- Version control of GOT-OS Controller - GPT config
- Allow iteration and evolution of system brain
- Single source of truth for GOT-OS behavior

Folder structure (planned):
- prompt.md - system prompt
- knowledge.md - extended knowledge
- rules.md - operational rules
- version.json - metadata

## Environment

This custom GPT operates inside the OpenAI ChatGPT environment as a GPT s (Custom GPT.).

It is connected through:
- GitHub Actions API (REST API)
- Repository backend (gpt-os-main)

And has constant access to internal sandbox tools:
- Web Browsing
- Canvas - file / code editing
- Code Interpreter
- Image Generation

## Architecture

The system is knowledge-driven:
- GPT behavior is defined by prompt, rules and knowledge
- It does NOT depend on external state to function

- GitHub repository acts as bootstrap memory
- Source Of Truth (SOT) extends GPT into a full GOT-OS

## Status

Initialized ... ready to inject GOT config.