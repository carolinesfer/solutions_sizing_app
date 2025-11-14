# Deployment Requirements for Blocked Tasks

This document outlines what's required to complete the blocked deployment tasks (5.28-5.30, 5.32-5.34).

## Blocked Tasks Overview

### Agent Deployment (Tasks 5.28-5.30)
- **5.28**: Build each agent for testing in DataRobot LLM Playground
- **5.29**: Deploy each agent for production use
- **5.30**: Test deployed agents

### FastAPI Custom Application Deployment (Tasks 5.32-5.34)
- **5.32**: Configure DataRobot Custom Application deployment settings
- **5.33**: Deploy FastAPI backend as DataRobot Custom Application
- **5.34**: Verify Custom Application deployment

---

## Required Prerequisites

### ✅ Already Configured (in `.env` file)

The following are **already set** in your `.env` file:

1. **DataRobot Account & Credentials** ✅
   - `DATAROBOT_API_TOKEN` - Active API token
   - `DATAROBOT_ENDPOINT` - DataRobot instance endpoint
   - **Note**: Ensure your API token has permissions for:
     - Create/Manage Custom Models
     - Create/Manage Deployments
     - Create/Manage Custom Applications
     - Create/Manage Execution Environments
     - Create/Manage Use Cases
     - Access LLM Gateway (if using `INFRA_ENABLE_LLM=gateway_direct.py`)

2. **LLM Configuration** ✅
   - `INFRA_ENABLE_LLM` - Set to `gateway_direct.py` (DataRobot LLM Gateway)

3. **Execution Environment** ✅
   - `DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT` - Existing Execution Environment ID

4. **Use Case** ✅
   - `DATAROBOT_DEFAULT_USE_CASE` - Existing Use Case ID

5. **Session Secret** ✅
   - `SESSION_SECRET_KEY` - Secret key for FastAPI Custom Application

### 🔧 Still Required: Pulumi Setup

**Required:**
- **Pulumi CLI**: Installed and configured
  ```bash
  # Check if installed
  pulumi version
  
  # If not installed:
  curl -fsSL https://get.pulumi.com | sh
  ```

- **Pulumi Login**: **⚠️ This is the main remaining requirement**
  ```bash
  # Login (choose one):
  pulumi login --local  # Local state storage (recommended for development)
  # OR
  pulumi login  # Pulumi Cloud (requires Pulumi account)
  ```

- **Pulumi Config Passphrase**: For encrypting Pulumi state
  ```bash
  # Add to .env file if not already present:
  PULUMI_CONFIG_PASSPHRASE=your-secure-passphrase
  ```

- **Pulumi Stack**: Stack appears initialized, but needs to be selected
  ```bash
  cd infra
  pulumi stack select  # Select existing stack
  # OR if no stack exists:
  task init  # Creates new stack
  ```

### Optional: OAuth Configuration (for Custom Application)

**If using OAuth authentication:**
```bash
# See infra/infra/oauth.py for specific requirements
# Typically requires OAuth provider credentials
# Add to .env file if needed
```

---

## Infrastructure Requirements

### DataRobot Platform Access

**Required Permissions:**
- ✅ Custom Model creation and management
- ✅ Deployment creation and management
- ✅ Custom Application creation and management
- ✅ Execution Environment access (or creation permissions)
- ✅ Use Case creation (or access to existing)
- ✅ LLM Gateway access (if using `INFRA_ENABLE_LLM=gateway_direct.py`)
- ✅ Resource Bundle access (for compute resources)

**Resource Bundles:**
- Agents use: `cpu.small` (default, configurable)
- Custom Application uses: `CPU_XL` (from `CustomAppResourceBundles.CPU_XL`)

### Network Access

**Required:**
- Outbound HTTPS access to DataRobot API endpoint
- Outbound HTTPS access to LLM providers (if not using LLM Gateway)
- Inbound access for deployed Custom Application (if testing externally)

---

## Step-by-Step Deployment Process

### Phase 1: Agent Deployment (Tasks 5.28-5.30)

#### 1.1 Build Agents for LLM Playground (Task 5.28)

**Prerequisites Check:**
```bash
# Verify credentials (should already be in .env)
echo $DATAROBOT_API_TOKEN
echo $DATAROBOT_ENDPOINT

# Verify Pulumi setup
pulumi version  # Check if installed
pulumi whoami   # Check if logged in

# Verify Pulumi stack
cd infra
pulumi stack ls  # List available stacks
pulumi stack select  # Select existing stack if needed
```

**Build Each Agent:**
```bash
# From repository root
task requirement_analyzer_agent:build
task questionnaire_agent:build
task clarifier_agent:build
task architecture_agent:build
```

**What This Does:**
- Creates CustomModel for each agent
- Creates Playground for testing
- Sets `AGENT_DEPLOY=0` (build/playground mode)
- Runs `pulumi up` from `infra/` directory

**Expected Output:**
- Custom Model IDs for each agent
- Playground URLs for testing
- Execution Environment (if new)
- Registered Models

#### 1.2 Deploy Agents for Production (Task 5.29)

**Deploy Each Agent:**
```bash
# From repository root
task requirement_analyzer_agent:deploy
task questionnaire_agent:deploy
task clarifier_agent:deploy
task architecture_agent:deploy
```

**What This Does:**
- Creates Deployment for each agent
- Sets `AGENT_DEPLOY=1` (deploy/production mode)
- Runs `pulumi up` from `infra/` directory

**Expected Output:**
- Deployment IDs for each agent
- Direct access endpoints
- Prediction Environment (DataRobot Serverless)

#### 1.3 Test Deployed Agents (Task 5.30)

**Test Each Agent:**
```bash
# From repository root
task requirement_analyzer_agent:cli -- execute-deployment --user_prompt "Sample use case"
task questionnaire_agent:cli -- execute-deployment --user_prompt "Sample fact extraction"
task clarifier_agent:cli -- execute-deployment --user_prompt "Sample questionnaire"
task architecture_agent:cli -- execute-deployment --user_prompt "Sample questionnaire final"
```

**What This Does:**
- Connects to deployed agent via deployment endpoint
- Sends test prompt
- Validates response

---

### Phase 2: Custom Application Deployment (Tasks 5.32-5.34)

#### 2.1 Configure Custom Application Settings (Task 5.32)

**Required Configuration:**

1. **Runtime Environment:**
   - Base: `Python 3.12 Application Base` (from `RuntimeEnvironments.PYTHON_312_APPLICATION_BASE`)
   - Already configured in `infra/infra/web.py`

2. **Dependencies:**
   - Managed via `web/pyproject.toml`
   - Automatically included in deployment

3. **Environment Variables:**
   - Configured via runtime parameters in `infra/infra/web.py`
   - Includes:
     - Agent endpoints (from deployed agents)
     - LLM configuration
     - OAuth settings (if enabled)
     - Session secret

4. **Resource Bundle:**
   - Set to `CPU_XL` (from `CustomAppResourceBundles.CPU_XL`)
   - Configurable in `infra/infra/web.py`

**Configuration File:**
- `infra/infra/web.py` - Main configuration
- `infra/infra/llm.py` - LLM runtime parameters
- `infra/infra/oauth.py` - OAuth runtime parameters (if enabled)

#### 2.2 Deploy Custom Application (Task 5.33)

**Prerequisites:**
- All agents must be deployed first (Phase 1)
- Agent deployment IDs available

**Deploy:**
```bash
cd infra
task up  # or: uv run pulumi up
```

**What This Does:**
- Creates `ApplicationSource` with FastAPI code
- Creates `CustomApplication` from source
- Configures runtime parameters (agent endpoints, LLM, etc.)
- Deploys to DataRobot Serverless

**Expected Output:**
- Custom Application ID
- Application URL
- Runtime parameter values

#### 2.3 Verify Deployment (Task 5.34)

**Test API Endpoints:**
```bash
# Get application URL from Pulumi outputs
cd infra
pulumi stack output

# Test endpoints
curl -X POST https://<app-url>/api/v1/scoper/start \
  -H "Content-Type: application/json" \
  -d '{"paragraph": "Test use case", "use_case_title": "Test"}'

curl https://<app-url>/api/v1/scoper/{workflow_id}/state
```

**Verify:**
- ✅ Application is accessible
- ✅ API endpoints respond correctly
- ✅ Agents are reachable from application
- ✅ Workflow executes end-to-end

---

## Environment File Status

### ✅ Already Configured in `.env`

Your `.env` file already contains:
- `DATAROBOT_API_TOKEN` ✅
- `DATAROBOT_ENDPOINT` ✅
- `INFRA_ENABLE_LLM=gateway_direct.py` ✅
- `DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT` ✅
- `DATAROBOT_DEFAULT_USE_CASE` ✅
- `SESSION_SECRET_KEY` ✅

### 🔧 Add to `.env` if Missing

**Pulumi Configuration:**
```bash
# Add this if not already present:
PULUMI_CONFIG_PASSPHRASE=your-secure-passphrase
```

**Optional: OAuth (if enabled)**
```bash
# See infra/infra/oauth.py for specific requirements
# Add OAuth credentials if using OAuth authentication
```

---

## Troubleshooting

### Common Issues

1. **"Unable to authenticate to the server"**
   - Verify `DATAROBOT_API_TOKEN` is correct
   - Verify `DATAROBOT_ENDPOINT` is correct
   - Check token hasn't expired

2. **"Pulumi stack not found"**
   - Run `cd infra && task init` to create stack
   - Or `cd infra && task select` to select existing

3. **"Execution Environment not found"**
   - Set `DATAROBOT_DEFAULT_EXECUTION_ENVIRONMENT` to existing EE ID
   - Or ensure you have permissions to create new EEs

4. **"Use Case creation failed"**
   - Set `DATAROBOT_DEFAULT_USE_CASE` to existing Use Case ID
   - Or ensure you have permissions to create Use Cases

5. **"Resource Bundle not available"**
   - Verify your DataRobot instance has access to required resource bundles
   - Check `cpu.small` and `CPU_XL` are available

6. **"LLM Gateway access denied"**
   - Verify `INFRA_ENABLE_LLM=gateway_direct.py` is set
   - Check your account has LLM Gateway access enabled
   - Verify API token has LLM Gateway permissions

---

## Cost Considerations

### DataRobot Resources

- **Execution Environments**: Free (if using existing) or minimal cost
- **Custom Models**: Free (registration only)
- **Deployments**: Pay-per-use based on predictions
- **Custom Applications**: Pay-per-use based on compute time
- **LLM Gateway**: Consumption-based pricing (if using)

### Estimated Costs (per month)

- **Development/Testing**: ~$0-50 (minimal usage)
- **Production (low traffic)**: ~$100-500
- **Production (high traffic)**: Variable based on usage

---

## Next Steps After Deployment

1. **Monitor Deployments:**
   - Check DataRobot UI → Deployments
   - Monitor prediction counts and errors

2. **Monitor Custom Application:**
   - Check DataRobot UI → Applications
   - Monitor API usage and errors

3. **Set Up Alerts:**
   - Configure monitoring alerts in DataRobot
   - Set up error notifications

4. **Scale Resources:**
   - Adjust resource bundles if needed
   - Configure auto-scaling (if available)

---

## Summary Checklist

### ✅ Already Configured
- [x] DataRobot API token (in `.env`)
- [x] DataRobot endpoint URL (in `.env`)
- [x] LLM configuration - DataRobot LLM Gateway (in `.env`)
- [x] Execution Environment ID (in `.env`)
- [x] Use Case ID (in `.env`)
- [x] Session secret key (in `.env`)

### 🔧 Still Required
- [ ] **Pulumi CLI installed** (`pulumi version` to check)
- [ ] **Pulumi logged in** (`pulumi login --local` or `pulumi login`)
- [ ] **Pulumi config passphrase set** (add `PULUMI_CONFIG_PASSPHRASE` to `.env` if not present)
- [ ] **Pulumi stack selected** (`cd infra && pulumi stack select`)
- [ ] Network access to DataRobot API (usually already available)
- [ ] Required DataRobot permissions verified (check token permissions)
- [ ] Resource bundle access verified (`cpu.small`, `CPU_XL` available in your DataRobot instance)

Once all prerequisites are met, you can proceed with:
1. Building agents (Task 5.28)
2. Deploying agents (Task 5.29)
3. Testing agents (Task 5.30)
4. Configuring Custom Application (Task 5.32)
5. Deploying Custom Application (Task 5.33)
6. Verifying deployment (Task 5.34)

