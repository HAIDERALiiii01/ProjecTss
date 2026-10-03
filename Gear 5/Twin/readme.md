# 🕵️ DealScout

<p align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDE2cGdmNXZmMXM0bXFibzV5cTJkcTl0d2J2cGEycjFrc3BjZHN6ayZlcD12MV9naWZzX3NlYXJjaCZjdD1n/z2D26GunfUK1W/giphy.gif" alt="DealScout" width="800"/>
</p>

> **Hate to bargain but love to code? 😎 You’re in the right place. Let AI hunt, predict, and deliver the best deals for you.**

---

## 🎯 What it does

TODO — **DealScout** is an autonomous AI-powered deal-finding system that scans products, analyzes their prices, predicts whether a deal is genuinely worthwhile, and identifies the best opportunity. It uses AI agents to make decisions autonomously and can notify the user when it finds a valuable deal.

---

## 📁 Files

| File / Folder | Description |
| --- | --- |
| `deploy.ipynb` | **deploy.ipynb** provides the steps required to deploy the fine-tuned pricing model to Modal. It guides you through setting up the Hugging Face and Modal credentials, configuring the required Modal secret, and deploying the pricing service. |
| `deal_scout.py` | **DealScout** is a Gradio-based interface for running the autonomous deal-finding agent. It continuously scans for deals, displays price estimates and discounts, streams agent logs in real time, and visualizes the underlying vector database. |
| `deal_agent.py` | **DealAgentFramework** manages the core deal-finding pipeline, including the ChromaDB product vector store, deal memory, and Planning Agent. It runs the agent, stores discovered opportunities, and provides product embeddings for visualization. |
| `autonomous_deal_scout.py` | **Autonomous DealScout** provides a Gradio interface for running the autonomous deal-finding agent. It continuously discovers and evaluates deals, displays results and live agent logs, visualizes product embeddings, and allows users to trigger deal notifications. |
| `autonmous_deal_agent.py` | **DealAgentFramework** manages the autonomous deal-finding pipeline using an Autonomous Planning Agent, ChromaDB, and persistent deal memory. It runs the agent, stores discovered opportunities, and generates 3D visualizations of the product embeddings. |
| `log_utils.py` | **log_utils.py** reformats agent logs by converting terminal ANSI colors into HTML styling, allowing colored logs to be displayed correctly in the Gradio interface. |
| `memory.json` | **memory.json** stores previously discovered deal opportunities, including product details, current price, estimated value, deal URL, and calculated discount. |
| `pricer_service.py` | **pricer_service.py** deploys the fine-tuned pricing model as a Modal service. It loads the model from Hugging Face, runs price predictions on a T4 GPU, and provides a remote interface for estimating the true value of products. |
| `requirements.txt` | All dependencies |
| `.env` | Environment variables (see [Environment variables](#-environment-variables)) |
| `.python-version` | Pinned Python version for the project |
| `deep_neural_network.pth` | Trained model weights (~2GB) — not included in repo, see [Getting started](#-getting-started) |
| `products_vectorstore/` | Vector database — not included in repo, see [Notes](#-notes) |

### `fine-tuning/`

| File | Description |
| --- | --- |
| `TRAINING.ipynb` | **TRAINING.ipynb** fine-tunes Llama 3.2 3B for product price prediction using QLoRA. It loads the training dataset, applies 4-bit quantization and LoRA, trains the model with TRL, tracks the run with Weights & Biases, and pushes the fine-tuned model to Hugging Face. |

### `agents/`

| File | Description |
| --- | --- |
| `agent.py` | **agent.py** defines the base `Agent` class used by all agents in the framework. It provides a consistent logging system that identifies each agent and displays its messages with custom colors. |
| `autonomous_planning_agent.py` | **AutonomousPlanningAgent** uses an LLM to autonomously scan for deals, estimate their true value, select the most compelling bargain, and notify the user. It coordinates the Scanner, Ensemble, and Messaging agents through tool calls. |
| `deals.py` | TODO |
| `deep_neural_network.py` | **deep_neural_network.py** implements the neural network used to estimate a product’s true market value. It converts product descriptions into features with `HashingVectorizer`, loads trained `.pth` weights, and performs price prediction using PyTorch. |
| `ensemble_agent.py` | **EnsembleAgent** combines three independent pricing models—a specialist model, a frontier model, and a neural network—to estimate a product’s true value. It preprocesses the product description and uses weighted predictions to produce the final price estimate. |
| `evaluator.py` | **evaluator.py** evaluates price prediction models by comparing predicted prices with actual prices. It calculates error, MSE, and R² scores, and generates interactive charts showing prediction accuracy and error trends. |
| `frontier_agent.py` | **frontier_agent.py** uses RAG with ChromaDB to find 5 similar products, then provides their prices as context to an OpenAI model to estimate the target product’s price. |
| `items.py` | **items.py** defines the `Item` data model for products, including their price and metadata. It also creates price-prediction prompts and handles saving/loading item datasets to and from the Hugging Face Hub. |
| `messaging_agent.py` | **messaging_agent.py** handles deal notifications by using GPT-5-mini to craft concise alerts and sending them to the user through ntfy push notifications. |
| `neural_network_agent.py` | **neural_network_agent.py** connects the Deep Neural Network inference model to the agent framework. It loads the trained model weights and uses the network to predict a product’s true price. |
| `planning_agent.py` | **planning_agent.py** orchestrates the fixed deal-finding workflow. It scans for deals, uses the Ensemble Agent to estimate their value, selects the best of up to 5 deals, and sends a notification when the discount exceeds $50. |
| `preprocesor.py` | **preprocessor.py** cleans and structures raw product text using an LLM. It converts unstructured listings into standardized fields such as title, category, brand, description, and details for more consistent price estimation. |
| `scanner_agent.py` | **scanner_agent.py** fetches new deals from RSS feeds and uses GPT-5-mini to select and summarize the 5 most promising deals with clear prices and detailed product descriptions. |
| `specialist_agent.py` | **specialist_agent.py** connects to a remotely hosted fine-tuned pricing model on Modal and uses it to estimate the true price of a product from its description. |

---

## ⚙️ How it works

## Pipeline / Agent Flow

DealScout follows a multi-agent pipeline where each agent has a specific job:

**1. Scanner Agent → Find Deals**  
The Scanner Agent fetches new deals from RSS feeds and uses **GPT-5-mini** to select the 5 most promising deals with clear prices and detailed product descriptions.

**2. Planning Agent → Coordinate the Workflow**  
The Planning Agent takes those 5 deals and sends each one to the Ensemble Agent for price estimation.

**3. Ensemble Agent → Estimate True Value**  
The Ensemble Agent combines three different pricing approaches:
- **Specialist Agent** — uses a fine-tuned pricing model hosted on Modal.
- **Frontier Agent** — uses RAG to find 5 similar products from ChromaDB and asks an OpenAI model to estimate the price.
- **Neural Network Agent** — uses a trained deep neural network to predict the price.

Their predictions are combined into a final estimated true value.

**4. Planning Agent → Find the Best Deal**  
For each deal, the system calculates:

`Discount = Estimated True Value − Deal Price`

The 5 opportunities are ranked by discount, and the deal with the highest discount is selected.

**5. Messaging Agent → Notify the User**  
If the best deal has a discount greater than **$50**, the Messaging Agent uses **GPT-5-mini** to create an exciting notification and sends it to the user through **ntfy**.

### Overall Flow

**RSS Feeds → Scanner Agent → 5 Deals → Planning Agent → Ensemble Agent → 3 Pricing Models → Estimated Value → Best Deal → Messaging Agent → Notification**

The **autonomous version** follows the same general pipeline, but instead of the workflow being hard-coded, the **Autonomous Planning Agent uses the LLM to decide which tools and agents to call and when**.

---

## 🚀 Getting started

### 1. Clone the repository

```bash
git clone https://github.com/HAIDERALiiii01/ProjecTss
cd "ProjecTss/Gear 5/DealScout"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Download the model weights

`deep_neural_network.pth` (~2GB) isn't in the repo. Download it from Google Drive and place it in the project root:

[Download deep_neural_network.pth](https://drive.google.com/drive/folders/1uq5C9edPIZ1973dArZiEO-VE13F7m8MK)

### 4. Set up environment variables

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=
GOOGLE_API_KEY=
HF_TOKEN=
MODAL_TOKEN_ID=
MODAL_TOKEN_SECRET=
NTFY_TOPIC=
```

### 5. Run DealScout

Before running DealScout, complete the setup in this order:

1. **Fine-tune the pricing model** using `TRAINING.ipynb`.
   - Configure your **Google Colab**, **Hugging Face**, and **Weights & Biases** tokens.
   - Train the Llama 3.2 3B pricing model using QLoRA.
   - The fine-tuned model is pushed to Hugging Face.

2. **Deploy the pricing model** using `deploy.ipynb`.
   - Configure your **Modal** credentials.
   - Set up the **Hugging Face secret** in Modal.
   - Deploy `pricer_service.py` to Modal.

3. **Run DealScout** using one of the two entry points:

   **Non-Autonomous Mode**
   ```bash
   python deal_scout.py
   ```
   Uses the predefined workflow with the **Planning Agent** to find, evaluate, rank, and notify about deals.

   **Autonomous Mode**
   ```bash
   python autonomous_deal_scout.py
   ```
   Uses the **Autonomous Planning Agent**, allowing the LLM to decide which tools and agents to use and when.

### Overall Setup Flow

**Google Colab → Fine-tune Model → Hugging Face → Modal Deployment → DealScout**

After deployment, you can choose between **Non-Autonomous** and **Autonomous** DealScout.

## 📦 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

## 🛠️ Key Libraries Used

- **OpenAI** — LLMs and agent-based workflows
- **Transformers** — Llama model loading and inference
- **TRL** — Fine-tuning with supervised fine-tuning (SFT)
- **PEFT** — LoRA/QLoRA fine-tuning
- **PyTorch** — Deep neural network training and inference
- **ChromaDB** — Vector storage and similarity search
- **scikit-learn** — Text processing, evaluation, and machine learning utilities
- **Gradio** — Web interface for DealScout
- **Modal** — Cloud deployment of the fine-tuned pricing model
- **Weights & Biases** — Training experiment tracking
- **Hugging Face Hub** — Dataset and fine-tuned model hosting
- **ntfy** — Push notifications for detected deals
- **python-dotenv** — Environment variable and API credential management
- **Feedparser / RSS** — Fetching deal feeds
---

## 📝 Notes

- **Environment:** `.venv/` and `__pycache__/` are excluded from the repository.
- **Vector Store:** `products_vectorstore/` is excluded. You can rebuild the ChromaDB vector store using the provided data and embedding pipeline.
- **Neural Network:** `deep_neural_network.pth` is excluded because of its large size (~2GB). Download it using the link provided above.
- **Secrets:** `.env` is excluded. Never commit API keys, tokens, or other credentials to GitHub.
- **API Providers:** DealScout is designed to be extensible. You can experiment with different LLM providers such as **OpenAI, Google Gemini, xAI Grok, or other compatible models** and improve the agents for your own use case.
- **Experiment Freely:** The existing agents, prompts, pricing models, and decision-making logic are starting points. You can modify them, add new agents, use different models, change the deal-selection strategy, or build additional features.
- **Pricing Models:** The Ensemble Agent can be extended with additional pricing models or different weighting strategies to improve price estimation.
- **Autonomous Mode:** The autonomous version gives the LLM more control over the workflow, making it a good starting point for experimenting with more advanced agentic behavior.
- **Notifications:** The messaging system can be adapted to other notification services instead of `ntfy`.
- **Customization:** You can change the RSS sources, product categories, pricing models, notification method, prompts, and agent workflow to turn DealScout into your own personal deal-finding system.

> **The project is meant to be explored and improved. Don't treat the current implementation as the limit — swap models, add agents, change the workflow, and see what you can build.** 🚀

> **"Just because something works that doesn't mean it cannot be improved".** 