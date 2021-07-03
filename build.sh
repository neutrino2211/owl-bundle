for x in apps/*; do
	cd "$x"
	echo "Removing $x/dist"
	rm -rf "$x/dist"
	npm run build
	cd ../..
	python3 bundle.py "$x"
done

for app in *.app; do
	mv "$app" outputs
done

python3 FQL.py pack outputs
mv outputs.fz ~/Desktop/OWL-OS/install/apps.fz