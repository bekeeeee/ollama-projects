import {
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  MessagesPlaceholder,
} from "@langchain/core/prompts";
import {ConversationChain} from "langchain/chains";

import {ChatOllama} from "@langchain/ollama";
import {
  ConversationSummaryBufferMemory,
  ChatMessageHistory,
} from "langchain/memory";

const llm = new ChatOllama({
  model: "deepseek-r1:1.5b", // specify the model to use
  temperature: 0.7, // adjust the temperature for response variability
});

let memory = new ConversationSummaryBufferMemory({
  memoryKey: "messages", // key under which the messages will be stored
  returnMessages: true, // return messages instead of just the text
  llm,
  chatHistory: new ChatMessageHistory(),
});
const prompt = new ChatPromptTemplate({
  inputVariables: ["content", "messages"],
  promptMessages: [
    new MessagesPlaceholder("messages"),
    HumanMessagePromptTemplate.fromTemplate("{content}"),
  ],
});

const chain = new ConversationChain({
  llm,
  prompt,
  memory,
  outputKey: "text",
  verbose: true, // enable verbose logging
});

(async () => {
  while (true) {
    // get user input from the terminal by node:readline
    const userInput = await new Promise<string>(resolve => {
      const readline = require("node:readline").createInterface({
        input: process.stdin,
        output: process.stdout,
      });
      readline.question("Enter your question: ", (input: string) => {
        readline.close();
        resolve(input);
      });
    });

    const response = await chain.invoke({content: userInput});
    console.log(
      "Response:",
      response.text.replace(/<think>[\s\S]*?<\/think>\n?/g, "").trim()
    );
    console.log("-------------------------------------");
    // Log the memory state
    console.log("Memory State:");
    const messages = await memory.loadMemoryVariables({});
    // console.log("Messages in memory:", Object.keys(messages));
    // console.log("messages:", messages.messages);
    if (!messages || messages.messages.length === 0) {
      console.log("No messages in memory.");
      console.log("-------------------------------------");

      continue;
    }
    // messages.messages.forEach((message: any, index: number) => {
    //   console.log(
    //     `Message ${index + 1}:`,
    //     message.text.replace(/<think>[\s\S]*?<\/think>\n?/g, "").trim()
    //   );
    // });
    // console.log("Total messages in memory:", messages.messages.length);
    // console.log(
    //   "Last message in memory:",
    //   messages.messages[messages.messages.length - 1]?.text
    //     .replace(/<think>[\s\S]*?<\/think>\n?/g, "")
    //     .trim()
    // );
    // console.log("-------------------------------------");
  }
})();
