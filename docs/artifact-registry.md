# **Artifact Registry & Workload Identity Federation for CI/CD**

## **Overview**
In this assignment, we will use **Google Cloud's Artifact Registry** to store and manage Docker container images, and configure **Workload Identity Federation** to authenticate our __GitHub Actions workflows__ with Google Cloud securely. This ensures that our CI/CD pipelines can push Docker images without relying on long-lived service account keys.

Your task is to complete the GitHub Actions workflow file [`ci.yml`](../.github/workflows/ci.yml) by uncommenting and properly configuring the steps required to:
1. **Authenticate to Google Cloud** using Workload Identity Federation
2. **Configure Docker to push to Artifact Registry**
3. **Build and push the Docker image to Artifact Registry**

---

## **1. What is Workload Identity Federation?**
[Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation) enables **GitHub Actions to authenticate with GCP** using OpenID Connect (**OIDC**) **without** long-lived service account keys. This is the preferred authentication method because it enhances security by eliminating hardcoded credentials.

🔹 **How it works:**
- GitHub Actions sends **OIDC tokens** to Google Cloud.
- Google Cloud verifies the identity and grants temporary credentials.
- These credentials allow **pushing Docker images** to Artifact Registry.

📌 **Follow this tutorial to set up Workload Identity Federation:**  
[Direct Workload Identity Federation](https://github.com/google-github-actions/auth?tab=readme-ov-file#preferred-direct-workload-identity-federation)

📝 **Note:** You will need to grant the `roles/artifactregistry.createOnPushWriter` **Role** to the Service Account that the Workload Identity Pool is configured to use.

---

## **2. What is Google Cloud Artifact Registry?**
[Artifact Registry](https://cloud.google.com/artifact-registry) is Google Cloud’s secure storage solution for container images and other build artifacts. It replaces **Container Registry** and offers better security, performance, and regional availability.

In this assignment, you will:
- Create a **Docker Artifact Repository** in Google Cloud.
- Push Docker images from GitHub Actions to this repository.
- Retrieve stored images for deployment in cloud environments.

📌 **Follow this tutorial to create your Docker Artifact Repository:**  
[Create Docker Artifact Registry](https://cloud.google.com/artifact-registry/docs/repositories/create-repos#create-repo-gcloud-docker)  

📝 **Note:** You will need the **repository URL** and **region** for configuring the GitHub Actions workflow.

---

## **3. Completing the GitHub Actions Workflow**
The [`ci.yml`](../.github/workflows/ci.yml) file contains a **partially completed workflow** for building and pushing Docker images to Artifact Registry. You need to **uncomment and configure** the missing steps.

### **🔹 Key Sections to Complete**
1. **Authenticate with Google Cloud using Workload Identity Federation**
   ```yaml
   #      - uses: 'google-github-actions/auth@v2'
   #        id: auth
   #        name: Authenticate to GCP
   #        with:
   #          project_id: 'my-project'
   #          workload_identity_provider: 'YOUR WORKLOAD PROVIDER projects/012345678901/locations/global/workloadIdentityPools/github-actions/providers/dansc0de'
   ```
   📌 **Replace placeholders (`YOUR Project ID`, `YOUR WORKLOAD PROVIDER`) with actual values.**  
   
2. **Configure Docker to push to Artifact Registry**
   ```yaml
   #      - name: gcloud Configure Docker
   #        run: gcloud auth configure-docker [YOUR REGION e.g. us-central1]-docker.pkg.dev
   ```
   📌 **Update `[YOUR REGION]` to match your Artifact Registry's region.**

3. **Build and push the Docker image**
   ```yaml
   #      - name: Build and Push
   #        uses: docker/build-push-action@v6
   #        with:
   #          context: ./
   #          file: ./Dockerfile
   #          push: true
   #          tags: [YOUR REGION e.g. us-central1]-docker.pkg.dev/cc-spring2025/dansc0de/fastapi-server:v2
   ```
   📌 **Ensure the tag matches your Artifact Registry format.**

---

## **4. Running the CI/CD Workflow**
Once you have configured and committed your changes:
1. Push your changes to GitHub.
2. The **GitHub Actions workflow** will automatically execute on every push.
3. The **Docker image** will be built and pushed to Artifact Registry.

---

## Helpful commands

### List Artifact Repositories
Use this command to list all Artifact Registries in your GCP project. Replace [PROJECT ID] and [REGION] with your specific values.

```shell
 gcloud artifacts repositories list --project=[PROJECT ID] --location=[REGION]
```

### Verify Permissions on Artifact Registry
This command checks the IAM policy for your Artifact Registry. Ensure your Workload Identity Pool has the correct permissions to push Docker images.

```shell
gcloud artifacts repositories get-iam-policy [Container Registry Name] \
  --location=us-central1 \
  --project="${PROJECT_ID}"
```

### Bind Role To PrincipleSet on Artifact Registry
```shell
gcloud artifacts repositories add-iam-policy-binding [Artifact Registry] \
  --location=[REGION] \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_ID_POOL}/attribute.repository/${REPO}" \
  --role="roles/artifactregistry.createOnPushWriter" \
  --project="${PROJECT_ID}"
```