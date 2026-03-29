# GPT-OS Controller

This folder contains the complete custom GPT configuration for GPT-OS Controller.

It is a 1:1 representation of the GPT definition (parameters, rules, knowledge) used inside ChatGPT.

## Purpose

- Single source of truth for GPT-OS Controller
- Allow evolution of GPT behavior via repo
- Enable controller upgrades without rebuilding system

## File Descriptions

## 00_bootstrap.md
Initialization logic for GPT-OS. Defines how the controller bootstraps itself from repository.

## 01_auto_debug.md
Self-healing system definition. Contains debug flow, error detection and fix strategies.

## 03_execution.md
Execution model for GOT-OS. Defines events, workflows and async execution.

## 04_command_mapping.md
Mapping between user intent and actions. Defines how commands are interpreted.

## 05_command_contract.json
Structured definition of command contracts. Used for deterministic execution.

## 06_auto_evolution.md
System evolution logic. Defines how GPT-OS can improve itself.

## 07_governor.md
Rules for system control and priority. Ensures stability and safety.

## 08_roles.md
Definition of internal roles and modules within GOT-OS.

## 09_async_dispatch.md
Asynchronous execution and dispatch logic. Enables event-driven architecture.

## 10_system_awareness.md
System state awareness. Defines how GOT-OS tracks its state and context.

## 11_semantic_routes.json
Seantic routing map in multi-language. Maps user intents to commands.

## Additional Files

## README.md
Overview of the controller and environment.

## prompt.md
Core system prompt used by the GPT.

## tools_openapi_schema.yaml
OpenAPI schema for GitHub API integration.

## Architecture

This system is knowledge-driven and bootstrapped from the repository.
