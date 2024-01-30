def bold(text):
    start ='\033[1m'
    end='\033[0m'
    return start+text+end

def red(text):
    start ='\033[91m'
    end='\033[0m'
    return start+text+end

def blue(text):
    start ='\033[94m'
    end='\033[0m'
    return start+text+end
