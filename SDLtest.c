#include <SDL/SDL.h>
 
int main(int argc, char** argv) {
  SDL_Init(SDL_INIT_EVERYTHING);
  SDL_Surface *screen;
 
  screen = SDL_SetVideoMode( 480, 320, 16, SDL_SWSURFACE );
  SDL_Rect rect;
	rect.x = 100;
	rect.y = 100;
	rect.w = 200;
	rect.h = 200;
 
	Uint32 color = SDL_MapRGB(screen->format, 0xff,0xff,0xff);
		SDL_FillRect(screen, &rect, color);
	SDL_Flip(screen);
	getchar();
 
	SDL_Quit();
	return 0;
}

# Compile with 
# 		gcc -o test test.c `sdl-config –cflags` `sdl-config –libs` -lSDL

# Run with
#			sudo ./test
