import persist_bool as pb

parser = pb.SentimentAnalyzer()

test_input = "I mean, come on, if he was really that into Nazism, wouldn't we have seen him sporting a swastika tattoo or something by now? Nope. He's just a guy who likes to talk about his own genius and thinks he's above criticism. That's not Nazism, folks."

result = parser.parse(test_input)
scores = parser.get_scores(test_input)

print(f'result : {result}')
print(f'scores : {scores}')