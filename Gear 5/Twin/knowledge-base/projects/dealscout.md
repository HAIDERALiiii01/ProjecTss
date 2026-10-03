---
type: project
name: DealScout
topics: [agents, rag, fine-tuning, neural-network, ensemble, autonomous-workflow]
stack: Python, Llama 3.2 3B, QLoRA, PyTorch, ChromaDB, OpenAI, Modal, Gradio, ntfy
repo: https://github.com/HAIDERALiiii01/ProjecTss/tree/main/Gear%205/DealScout
---

# DealScout: Autonomous AI Deal Finder

## What DealScout is and why I built it

DealScout is an autonomous AI deal-finding system that I built. It scans product deals from RSS feeds, estimates what each product is actually worth, finds deals that look underpriced, and notifies me when it finds a valuable one.

I built DealScout to bring together many things I had learned instead of using them separately: LLM agents, RAG, a fine-tuned language model, a neural network, ensemble prediction, tool calling, autonomous planning, cloud deployment, and push notifications. It was a way to see how these techniques work together as one complete system.

## How the DealScout pipeline works

In DealScout, the general flow is: RSS feeds, then the Scanner, then deal selection, then price estimation, then deal comparison, then the best opportunity, then a notification.

For each deal, the discount is calculated as the estimated true value minus the deal price. The five candidate deals are ranked by discount and the highest one is selected. If that discount is greater than $50, I get a notification.

DealScout has two modes. The non-autonomous mode follows a predefined workflow controlled by the Planning Agent. The autonomous mode lets the LLM decide which tools and agents to use and when.

## The Scanner Agent

In DealScout, the Scanner Agent fetches new deals from RSS feeds. It uses GPT-5-mini to select and summarize the five most promising deals, producing product information such as the name, price, and description.

## The Planning Agent (fixed workflow)

In DealScout, the Planning Agent controls the fixed, non-autonomous workflow. It sends the five selected deals to the Ensemble Agent for price estimation, compares each estimated value with the actual deal price, and picks the deal with the highest discount. If the discount is over $50, it calls the Messaging Agent. The sequence is always Scanner, Ensemble, select best deal, Messaging.

## The Ensemble Agent and the three pricing signals

In DealScout, the Ensemble Agent estimates a product's true value by combining three independent pricing approaches: a fine-tuned model, a RAG-based frontier model, and a custom neural network. I used all three because I had learned each technique and wanted to combine their strengths instead of relying on only one.

Before pricing, the Ensemble Agent runs the product description through a preprocessing step that rewrites the text, and all three models price that rewritten version. It then combines their predictions as a weighted average with fixed weights: 80% for the RAG-based frontier model, 10% for the fine-tuned Llama model, and 10% for the neural network. The weights are set in code, so the frontier model has by far the most influence on the final price.

## The fine-tuned pricing model (Specialist Agent)

In DealScout, the Specialist Agent uses a Llama 3.2 3B model that I fine-tuned for product price prediction. This is the part of DealScout I am most proud of.

I fine-tuned it with QLoRA, using 4-bit quantization and LoRA, trained with TRL and tracked with Weights & Biases. After training, I pushed the model to Hugging Face and deployed it on Modal, where inference runs on a T4 GPU. The deployment flow was Google Colab, then fine-tuning, then Hugging Face, then Modal, then DealScout.

## The RAG pricing model (Frontier Agent)

In DealScout, the Frontier Agent estimates prices with retrieval-augmented generation. It searches a ChromaDB product vector store for the five most similar products and gives their prices as context to an OpenAI model, which estimates the target product's value. This lets the system use comparable products as evidence.

DealScout also keeps a persistent deal memory in memory.json. It stores previously found opportunities, including the product, current price, estimated value, deal URL, and calculated discount. The product vector store and the neural network weights are not in the repository because of their size, so they are generated or downloaded separately.

## The neural network (Neural Network Agent)

In DealScout, the Neural Network Agent connects the agent framework to a custom PyTorch neural network that I trained. It turns product descriptions into features with HashingVectorizer and predicts the product's estimated true value. It is the third independent pricing signal in the ensemble.

## The Messaging Agent and notifications

In DealScout, the Messaging Agent handles notifications. When the estimated discount exceeds the $50 threshold, GPT-5-mini writes a concise alert and the message is sent to me through ntfy push notifications.

## Fixed workflow vs autonomous workflow

DealScout shows two ways of orchestrating agents in the same system. The key difference is who controls the workflow: in fixed mode, the workflow controls the AI, and in autonomous mode, the AI controls the workflow.

In the autonomous version, the Autonomous Planning Agent uses an LLM to decide which tools and agents to call and when, instead of following a fixed sequence. It coordinates the Scanner, Ensemble, and Messaging capabilities through tool calls. This is the main agentic-AI part of DealScout.

## The DealScout interface

I built DealScout's interface with Gradio. It can run the deal-finding system, show price estimates and discounts, stream agent logs in real time, run the autonomous version, trigger notifications, and show a 3D visualization of the product embeddings behind the vector database.

## The hardest part of building DealScout

The hardest part of DealScout was putting everything together into one working system. Fine-tuning the model was not the hardest part. The real challenge was integrating the different models and agents so the whole pipeline could go from discovering a deal, to estimating its value, to selecting an opportunity, to notifying me.

## What I learned from DealScout

DealScout helped me understand how different AI techniques can be combined into a larger system, instead of treating agents, RAG, fine-tuning, neural networks, and tool calling as separate concepts. It also gave me hands-on experience with the difference between a fixed agent workflow and an autonomous one where an LLM controls the tools.

## Technologies used in DealScout

- AI and ML: Llama 3.2 3B, GPT-5-mini, OpenAI models, PyTorch, QLoRA, LoRA/PEFT, TRL, Scikit-learn
- Retrieval: ChromaDB, embeddings, similarity search
- Infrastructure: Modal, Hugging Face, Google Colab, Weights & Biases
- Application: Python, Gradio, ntfy, RSS with Feedparser