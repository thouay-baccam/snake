import pygame
import sys
import random

# Initialisation des paramètres du jeu
LARGEUR, HAUTEUR = 800, 600
TAILLE_CASE = 50
FPS = 7
ZONE_JEU = (700, 500)
COULEURS = {
    "fond": (202, 220, 159),
    "fond_jeu": (173, 216, 230),
    "serpent": (48, 98, 48),
    "tete_serpent": (15, 56, 15),
    "pomme": (255, 255, 255),
    "texte": (0, 0, 0)
}
X_CENTRE_JEU, Y_CENTRE_JEU = (LARGEUR - ZONE_JEU[0]) // 2, (HAUTEUR - ZONE_JEU[1]) // 2

# Initialisation de Pygame
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake? SNAAAAAAAAAAKE")
horloge = pygame.time.Clock()

# Initialisation des scores
score = 0
highscore = 0

# Fonctions du jeu
def placer_pomme(serpent):
    while True:
        x_pomme = random.randint(X_CENTRE_JEU // TAILLE_CASE, (X_CENTRE_JEU + ZONE_JEU[0] - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        y_pomme = random.randint(Y_CENTRE_JEU // TAILLE_CASE, (Y_CENTRE_JEU + ZONE_JEU[1] - TAILLE_CASE) // TAILLE_CASE) * TAILLE_CASE
        pomme = (x_pomme, y_pomme)
        if pomme not in serpent:
            return pomme

def afficher(serpent, pomme, score, highscore):
    ecran.fill(COULEURS["fond"])
    pygame.draw.rect(ecran, COULEURS["fond_jeu"], (X_CENTRE_JEU, Y_CENTRE_JEU, ZONE_JEU[0], ZONE_JEU[1]))
    pygame.draw.rect(ecran, COULEURS["pomme"], (*pomme, TAILLE_CASE, TAILLE_CASE))

    for i, partie in enumerate(serpent):
        couleur = COULEURS["tete_serpent"] if i == 0 else COULEURS["serpent"]
        pygame.draw.rect(ecran, couleur, (*partie, TAILLE_CASE, TAILLE_CASE))

    font = pygame.font.Font(None, 40)
    texte_score = font.render(f"Score: {score}  Highscore: {highscore}", True, COULEURS["texte"])
    rect_score = texte_score.get_rect(center=(LARGEUR / 2, 30))
    ecran.blit(texte_score, rect_score)
    pygame.display.flip()

def game_over():
    global score
    font = pygame.font.Font(None, 36)
    texte = font.render(f"Game Over - Score final: {score} - Appuyez sur ESPACE pour rejouer", True, COULEURS["texte"])
    rect = texte.get_rect(center=(LARGEUR / 2, HAUTEUR / 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                jeu_serpent()

        ecran.fill(COULEURS["fond"])
        ecran.blit(texte, rect)
        pygame.display.flip()
        horloge.tick(5)

def jeu_serpent():
    global score, highscore
    serpent = [(X_CENTRE_JEU, Y_CENTRE_JEU)]
    direction = (1, 0)
    pomme = placer_pomme(serpent)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)

        nouvelle_tete = (serpent[0][0] + direction[0] * TAILLE_CASE, serpent[0][1] + direction[1] * TAILLE_CASE)
        serpent.insert(0, nouvelle_tete)
        if nouvelle_tete == pomme:
            pomme = placer_pomme(serpent)
            score += 1
            highscore = max(score, highscore)
        else:
            serpent.pop()

        if (
            nouvelle_tete[0] < X_CENTRE_JEU or
            nouvelle_tete[0] >= X_CENTRE_JEU + ZONE_JEU[0] or
            nouvelle_tete[1] < Y_CENTRE_JEU or
            nouvelle_tete[1] >= Y_CENTRE_JEU + ZONE_JEU[1] or
            nouvelle_tete in serpent[1:]
        ):
            game_over()

        afficher(serpent, pomme, score, highscore)
        horloge.tick(FPS)

# Lancement du jeu
jeu_serpent()