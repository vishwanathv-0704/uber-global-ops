# ---------------------------------------------------------
# Day 3 Conversational Memory
# ---------------------------------------------------------

class ConversationMemory:
    """
    Simple short-term conversational memory.

    Stores recent user messages and assistant responses so that
    follow-up questions can retain context.
    """

    def __init__(self, max_history=10):
        self.max_history = max_history
        self.history = []

    def add_message(self, role, content):
        """
        Add a message to conversation history.
        """

        self.history.append({
            "role": role,
            "content": content
        })

        # Keep only the most recent messages
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self):
        """
        Return the complete conversation history.
        """

        return self.history

    def get_context(self):
        """
        Convert conversation history into text context
        for the LLM.
        """

        if not self.history:
            return ""

        context = []

        for message in self.history:
            role = message["role"].upper()
            content = message["content"]

            context.append(
                f"{role}: {content}"
            )

        return "\n".join(context)

    def clear(self):
        """
        Clear conversation history.
        """

        self.history = []


# ---------------------------------------------------------
# Manual Test
# ---------------------------------------------------------

if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Check SFO"
    )

    memory.add_message(
        "assistant",
        "SFO completion rate is 71%."
    )

    memory.add_message(
        "user",
        "What about its surge?"
    )

    print("=" * 60)
    print("DAY 3 MEMORY TEST")
    print("=" * 60)

    print(memory.get_context())
