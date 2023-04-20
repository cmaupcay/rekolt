default_target: all
.PHONY : default_target

all: clean cmake run
.PHONY : all

sync: 
	@-base -f sync . 
	@echo [tensaiji.rekolt] Projet synchronisé.
.PHONY : sync

clean: clean.cmake clean.pycache
	@echo [tensaiji.rekolt] Dossier nettoyé.
.PHONY : clean

cmake: 
	@-mkdir -p cmake && cd cmake && cmake ..
.PHONY : cmake

cible: cmake
	@-cd cmake && make
.PHONY : cible

clean.cmake: 
	@-rm -rf cmake
.PHONY : clean.cmake

clean.cible: 
	@-rm -rf bin
.PHONY : clean.cible

run: 
	@-python -m rekolt
.PHONY : run

maj.git:
	@-git pull

maj: maj.git clean make

clean.pycache: 
	@-find . | grep -E "__pycache__" | xargs rm -rf
.PHONY : clean.pycache

clean.dest: 
	@-rm -rf dest
.PHONY : clean.dest

install: 
	@-pip install --upgrade -r requirements.txt
.PHONY : install

