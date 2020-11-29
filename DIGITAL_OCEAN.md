# DigitalOcean Deployment Guide

This is a short walkthrough of how to deploy this project on DigitalOcean. There are some manual steps, but everything is automated through GitLab CI as much as possible.

## DigitalOcean Setup

- Create SSH key for user with Digital Ocean and add it to your account
- Create a project
- Add any size Droplet with Docker 19.03.12 machine image, add the SSH key that you created
- Don't add any volumes (we will do that automatically with REX-Ray)
- Ceate a DigitOcean Personal Access Token and store it somewhere, we will use it later

## GitLab Setup

### Protected Tags

Go to `Settings > Repository > Protected Tags` and create a wildcard tag to protect. I use `rc*` for staging environments and `v*` for version. When I create a git tag such as `rc1.2.3`, the GitLab CI pipline will run since I have set the following in `gitlab-ci.yml`:

```yaml
workflow:
  rules:
    - if: "$CI_COMMIT_TAG =~ /^rc/"
      when: always
```

### Environment Variables

Add the following environment variables to the cloned GitLab project's `CI/CD > Variables` section.

Make sure the environment variables are all protected since they contain sensitive information.

- `DJANGO_SUPERUSER_EMAIL`

- `DJANGO_SUPERUSER_PASSWORD`

- `DJANGO_SUPERUSER_USERNAME`

- `DOMAIN_NAME`

I will be using domains from Freenom which are completely free to use, suitable for demonstrations or other types of projects where you don't want to pay for a `.com` or other paid domain.

- `READ_REGISTRY_TOKEN`

Create a GitLab Personal Access [https://gitlab.com/-/profile/personal_access_tokens](https://gitlab.com/-/profile/personal_access_tokens) and add it to this variable.

- `SSH_PRIVATE_KEY`

Add the private SSH key from the SSH key pair created earlier

- `DROPLET_IP`

- `POSTGRES_PASSWORD`

- `SECRET_KEY`

- `DEBUG`: set this to the value `0`


## DNS Setup

Create an A Record that points to the Droplet IP.

If you registered `mysite.ga` and your Droplet IP is `123.456.789.10`, make sure that you can see the Droplet IP address when you run `dig mysite.ga` from your terminal. It should contain the following lines:

```
;; ANSWER SECTION:
mysite.ga.		3600	IN	A	123.456.789.10
```

## Docker Swarm Setup

SSH into the Droplet:

```
ssh -i ~/.ssh/your-key root@123.456.789.10
```

### Install REX-Ray Plugin

Using the DigitalOcean personal access token you create earlier (NOT the GitLab personal access token), run the following command:

```
docker plugin install rexray/dobs DOBS_TOKEN=your-token-123abc DOBS_REGION=nyc1 LINUX_VOLUME_FILEMODE=0775
```

Replacing `your-token-123abc` with the actual token value.

Confirm that you would like to install by pressing `y`.

Verify that the plugin has been installed by running:

```
docker plugin lsID                  NAME                 DESCRIPTION                               ENABLED
2acafbb251e4        rexray/dobs:latest   REX-Ray for Digital Ocean Block Storage   true
```

### Initialize Docker Swarm

```
docker swarm init --advertise-addr 123.456.789.10
```

If you are going to use only one node for your swarm cluster, you can ignore the output of this command for now.

### Add traefik network

```
docker network create --driver=overlay traefik-public
```
