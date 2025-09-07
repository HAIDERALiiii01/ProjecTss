
import time
import os
from plyer import notification
import random

quotes = [
    "If you want to do great things in your life, then do what you love to do.",
    "Your mind is wired to resist change.",
    "Attachment is the root of suffering.",
    "Discipline is hard, but the pain of being average is harder.",
    "Believe in the very air that surrounds you.",
    "What you seek is within you—if only you reflect.",
    "No dreams, then no future.",
    "No failure, then no success.",
    "If you're tired, then do it tired.",
    "As long as you are alive, there are infinite chances.",
    "Push past your limits.",
    "Life rewards those who dare to step into the unknown.",
    "Talent without hard work is nothing.",
    "Do you see how infinite you are?",
    "Nothing gets easier; you just get better.",
    "You are too concerned with what others think.",
    "You are too concerned with what is and what will be.",
    "A lie travels faster than the truth.",
    "Our brain is for thinking, not for storing.",
    "Allow yourself to shine without the desire to be seen.",
    "We become what we think about.",
    "Until it’s done, tell none.",
    "There are plenty of fish in the sea.",
    "There are no limits to your imagination.",
    "There is no limit to the human brain.",
    "Be so good that they can’t ignore you.",
    "Focus on yourself; people come and go.",
    "When there is no enemy within, the enemy outside can do us no harm.",
    "You are built for greatness because you are created by the Greatest.",
    "A person chosen by God will never be chosen by humans.",
    "Sometimes the grass is greener because it's fake.",
    "In a war of ego, the loser always wins.",
    "Everything happens when you are busy.",
    "Don’t be afraid to stand alone.",
    "Doing nothing means doing absolutely nothing.",
    "The greatest thing in the world is to know how to be oneself.",
    "You don’t rise by feeling ready; you rise by deciding it’s time.",
    "If you don’t put effort into it, why even do it?",
    "Nothing changes if nothing changes.",
    "Don’t let toxic people rent space in your head.",
    "If you only do what you can do, you’ll never be more than you are.",
    "Chase your dreams, not people.",
    "When the kindest one loses control, it becomes a beast.",
    "A single word can brighten the face of one who knows the value of words.",
    "Never let loneliness drive you back to toxic people.",
    "Satisfy your soul, not society.",
    "It’s only when we embrace who we are that we can truly be free.",
    "We can’t hide from ourselves.",
    "If you think tough men are dangerous, wait until you see what weak men are capable of.",
    "It’s not about the destination; it’s about the journey.",
    "To achieve something extraordinary, you cannot allow yourself to be ordinary.",
    "Humans are equal in death.",
    "A wound that won’t kill you is nothing to be scared of.",
    "You either run from things or you face them.",
    "It’s all about accepting who we really are.",
    "Speak only to those who value your words.",
    "Once you hit the lowest point in your life, you realize you don’t need anyone.",
    "Pray for the best, prepare for the worst.",
    "Face your fears.",
    "Don’t listen to those voices in your head.",
    "You can’t heal in the same place that broke you.",
    "Anything you lose by being real was fake.",
    "Isolation is the price a man pays when he starts to fix his life.",
    "Purpose is more important than need.",
    "When death finds you, may it find you alive.",
    "Forgive others not because they deserve forgiveness, but because you deserve peace.",
    "The first to forget is the happiest.",
    "The first to forgive is the strongest.",
    "The first to apologize is the bravest.",
    "The thing about time is that it changes.",
    "Ultimately... we are all alone in this world.",
    "If you have eight hours to chop down a tree, spend six sharpening the axe.",
    "Discipline is nothing but self-respect at the highest level.",
    "If pain is the price of becoming the best, then let me suffer.",
    "God placed that dream in your heart because you can achieve it.",
    "Life is a struggle between the heart and the brain.",
    "Trust the process.",
    "An expert is a person who has made all the mistakes.",
    "Don’t worry about keeping it together; just keep it real.",
    "The road to heaven feels like hell.",
    "The road to hell feels like heaven.",
    "If a person knows more than others, he becomes lonely.",
    "Mental health is an everyday battle you need to win.",
    "No matter how dark it gets, never give up on yourself.",
    "Purpose of life? Simply to enjoy it all.",
    "The only thing we can control is mind over madness.",
    "In a world full of cruelty, we must hold on to our humanity.",
    "You have to die a few times before you can really live.",
    "If you are focused on the past, you are controlled by fear.",
    "Your biggest sin is that you destroyed and betrayed yourself for nothing.",
    "If you're afraid—don't do it. If you're doing it—don't be afraid.",
    "If truth shall kill them, let them die.",
    "The alone path teaches you a lot.",
    "Act according to your principles, not your mood.",
    "Never give up—great things take time.",
    "Great men are not born great; they grow great.",
    "The clock shows time, and time shows people.",
    "Problems are part of life; facing them is the art of life.",
    "Nobody cares as much as we fear they do.",
    "We often hold back, worrying about what others might think.",
    "It takes half of your life to discover that life is a do-it-yourself project.",
    "The person who asks a question is a fool for a minute; the person who doesn’t ask is a fool for life.",
    "You cannot live with your own failure.",
    "The sun will shine on us again.",
]



def create_log(message):
    log_path = os.path.join(os.getenv('TEMP'), 'quote_log.txt')
    with open(log_path, 'a') as f:
        f.write(f"{time.ctime()}: {message}\n")

def show_notification():
    try:
        quote = random.choice(quotes)
        notification.notify(
            title="DAILY MOTIVATION",
            message=quote,
            timeout=10,
            app_icon=None  # Remove if you get errors
        )
        create_log("Notification shown successfully")
    except Exception as e:
        create_log(f"Error: {str(e)}")

if __name__ == "__main__":
    create_log("Script started")
    show_notification()  # Immediate first notification
    
    while True:
        time.sleep(1800)  # 30 minutes
        show_notification()        
