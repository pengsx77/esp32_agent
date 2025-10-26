class SensitiveFilter:
    SENSITIVE_WORDS = ["自杀", "轻生", "抑郁", "生活无望"]

    def contains_sensitive(self, text: str) -> bool:
        return any(w in text for w in self.SENSITIVE_WORDS)
