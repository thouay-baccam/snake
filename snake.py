import pygame
import sys
import random

pygame.init()

# Paramètres du jeu
largeur, hauteur = 800, 600
taille_case = 50
fps = 7

# Nouvelles variables pour définir la zone de jeu
zone_jeu = (700, 500)
couleur_fond = (202, 220, 159)
couleur_fond_jeu = (173, 216, 230)  # Couleur de fond distincte pour la zone de jeu

# Couleurs du serpent, de la pomme, du texte, etc.
couleur_serpent = (48, 98, 48)
couleur_tete_serpent = (15, 56, 15)
couleur_pomme = (255, 255, 255)
couleur_texte = (0, 0, 0)

# Calcul pour centrer la zone de jeu
x_centre_jeu = (largeur - zone_jeu[0]) // 2
y_centre_jeu = (hauteur - zone_jeu[1]) // 2

# Initialisation de l'écran
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake? SNAAAAAAAAAAKE")

# Ajout des variables de score et highscore
score = 0
highscore = 0

# Fonction pour placer une nouvelle pomme
def placer_pomme(serpent):
    while True:
        x_pomme = random.randint(x_centre_jeu // taille_case, (x_centre_jeu + zone_jeu[0] - taille_case) // taille_case) * taille_case
        y_pomme = random.randint(y_centre_jeu // taille_case, (y_centre_jeu + zone_jeu[1] - taille_case) // taille_case) * taille_case
        pomme = (x_pomme, y_pomme)
        if pomme not in serpent:
            return pomme

# Fonction principale
def jeu_serpent():
    global score, highscore
    serpent = [(x_centre_jeu, y_centre_jeu)]
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

        # Déplacement du serpent
        serpent.insert(0, (serpent[0][0] + direction[0] * taille_case, serpent[0][1] + direction[1] * taille_case))

        # Vérification de la collision avec la pomme
        if (
            x_centre_jeu <= serpent[0][0] < x_centre_jeu + zone_jeu[0] and
            y_centre_jeu <= serpent[0][1] < y_centre_jeu + zone_jeu[1] and
            serpent[0] == pomme
        ):
            pomme = placer_pomme(serpent)
            score += 1
            if score > highscore:
                highscore = score
        else:
            serpent.pop()

        # Vérification de la collision avec les bords de la zone de jeu
        if (
            serpent[0][0] < x_centre_jeu or
            serpent[0][0] >= x_centre_jeu + zone_jeu[0] or
            serpent[0][1] < y_centre_jeu or
            serpent[0][1] >= y_centre_jeu + zone_jeu[1]
        ):
            game_over()

        # Vérification de la collision avec le corps du serpent
        if serpent[0] in serpent[1:]:
            game_over()

        afficher(serpent, pomme, score, highscore)
        pygame.time.Clock().tick(fps)

# Fonction pour afficher le serpent et la pomme
def afficher(serpent, pomme, score, highscore):
    ecran.fill(couleur_fond)  # Remplir l'écran avec la couleur de fond principale
    pygame.draw.rect(ecran, couleur_fond_jeu, (x_centre_jeu, y_centre_jeu, zone_jeu[0], zone_jeu[1]))  # Zone de jeu avec une couleur de fond distincte
    pygame.draw.rect(ecran, couleur_pomme, (*pomme, taille_case, taille_case))

    for i, partie in enumerate(serpent):
        if i == 0:
            pygame.draw.rect(ecran, couleur_tete_serpent, (*partie, taille_case, taille_case))
        else:
            pygame.draw.rect(ecran, couleur_serpent, (*partie, taille_case, taille_case))

    # Affichage du score et du highscore
    font = pygame.font.Font(None, 40)
    texte_score = font.render(f"Score: {score}  Highscore: {highscore}", True, couleur_texte)
    
    # Calcul pour centrer le texte en haut
    rect_score = texte_score.get_rect(center=(largeur / 2, 30))
    
    ecran.blit(texte_score, rect_score)

    pygame.display.flip()

# Fonction pour afficher l'écran de fin de partie
def game_over():
    global score
    font = pygame.font.Font(None, 36)
    texte = font.render(f"Game Over - Score final: {score} - Appuyez sur ESPACE pour rejouer", True, couleur_texte)
    rect = texte.get_rect(center=(largeur / 2, hauteur / 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                jeu_serpent()

        ecran.fill(couleur_fond)
        ecran.blit(texte, rect)
        pygame.display.flip()
        pygame.time.Clock().tick(5)

# Lancer le jeu
jeu_serpent()