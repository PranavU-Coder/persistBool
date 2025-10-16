import persistBool as pb

counter = pb.booleanPersistence()

text = "Oh, absolutely! Lets dive into this with some joyful curiosity! 😄✨ As of now, the President of India is Droupadi Murmu, and the Prime Minister is Narendra Modi."
result = counter.process_text(text)

final_answer = counter.parse()

print(f"{final_answer}")