import os

def save_best_score(points):
    if os.path.exists("dino_runner\components\list_score\score_text.txt"):
        with open("dino_runner\components\list_score\score_text.txt", "r") as f:
            best_score = int(f.read())
            if points > best_score:
                with open("dino_runner\components\list_score\score_text.txt", "w") as f:
                    f.write(str(points))
    else:
        with open("dino_runner\components\list_score\score_text.txt", "w") as f:
            f.write(str(points))
