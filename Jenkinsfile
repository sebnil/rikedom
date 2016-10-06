node {
	stage 'Checkout'
	checkout scm

	stage 'Install requirements'
    // bat 'conda install -c Quantopian zipline'
    bat 'pip install -r requirements.txt'

	stage 'Test'
	bat 'nosetests -w tests --with-xunit --with-coverage --cover-package=rikedom --verbosity=2'

	stage 'Archive'
	archive 'nosetests.xml'

	stage 'Publish'
	step([$class: 'JUnitResultArchiver', testResults: 'nosetests.xml'])
}
