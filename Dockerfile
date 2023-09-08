# Use the official PostgreSQL image from Docker Hub
FROM postgres:latest

# Set environment variables
ENV POSTGRES_DB ny_taxi
ENV POSTGRES_USER root
ENV POSTGRES_PASSWORD root

