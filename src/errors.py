class CallMeMaybeError(Exception):


class InputError(CallMeMaybeError):


class VocabError(CallMeMaybeError):


class GenerationError(CallMeMaybeError):


class OutputError(CallMeMaybeError):
