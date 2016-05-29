var gulp =        require('gulp');
var watch =       require('gulp-watch');
var clean =       require('gulp-clean');
var sass =        require('gulp-sass');
var minifycss =   require('gulp-clean-css');
var rename =      require('gulp-rename');
var livereload =  require('gulp-livereload');
var concat =      require('gulp-concat');
var uglify =      require('gulp-uglify');
var browserify =  require('browserify');

var bases = {
  dist: 'files/dist/'
};

var paths = {
  styles: [
    'files/static/scss/**/*.scss',
    'apps/*/scss/*.scss'
  ],
  js: [
    'files/static/js/**/*.js',
    'apps/**/js/*.js'
  ],
  files: {
    images: ['files/static/img/**/*'],
    files: ['files/static/files/**/*']
  },
  vendor: [
    'files/static/vendor/**/*'
  ],
  vendor_js: [
    'files/static/components/jquery/dist/jquery.min.js',
    'files/static/components/moment/min/moment-with-locales.min.js',
    'files/static/components/select2/dist/js/select2.full.min.js',
    'files/static/components/highlightjs/highlight.pack.min.js',
    'files/static/components/underscore/underscore-min.js'
  ]
};

var swallowError = function (error) {
  console.log('Swallowing Error');
  console.log(error.toString());
  this.emit('end');
};

/* Delete the dist directory */
gulp.task('clean', function () {
  return gulp.src(bases.dist)
    .pipe(clean())
});

/* Copy images */
var images = function () {
  return gulp.src(paths.files.images)
    .pipe(gulp.dest(bases.dist + 'img/'))
    .pipe(livereload());
};
gulp.task('images', ['clean'], images);
gulp.task('images-watch', images);

/* Copy files */
var files = function () {
  return gulp.src(paths.files.files)
    .pipe(gulp.dest(bases.dist + 'files/'))
    .pipe(livereload());
};
gulp.task('files', ['clean'], files);
gulp.task('files-watch', files);

/* Copy vendor */
var vendor_js = function () {
  return gulp.src(paths.vendor_js)
    .pipe(gulp.dest(bases.dist + 'vendor/js/')) // Remove if original files not wanted
    // .pipe(concat('vendor.min.js'))
    // .pipe(gulp.dest(bases.dist + 'vendor/'))
    .pipe(livereload());
};
gulp.task('vendor-js', ['clean'], vendor_js);
gulp.task('vendor-js-watch', vendor_js);

var vendor = function () {
  return gulp.src(paths.vendor)
    .pipe(gulp.dest(bases.dist + 'vendor/')) // Remove if original files not wanted
    // .pipe(concat('vendor.min.js'))
    // .pipe(gulp.dest(bases.dist + 'vendor/'))
    .pipe(livereload());
};
gulp.task('vendor', ['clean'], vendor);
gulp.task('vendor-watch', vendor);


/* Compile SCSS */
var sass_ = function () {
  return gulp.src(paths.styles)
    .pipe(sass())
    .on('error', swallowError)
    // .pipe(gulp.dest(bases.dist + 'css/')) // Remove is original files not wanted
    .pipe(rename('hakloevno.min.css'))
    .pipe(minifycss())
    .pipe(gulp.dest(bases.dist + 'css/'))
    .pipe(livereload());
};
gulp.task('sass', ['clean'], sass_);
gulp.task('sass-watch', sass_);

/* Compile JS */
var js = function () {
  return gulp.src(paths.js)
    // .pipe(gulp.dest(bases.dist + 'js/')) // Remove if original files not wanted
    .pipe(uglify())
    .on('error', swallowError)
    .pipe(concat('hakloevno.min.js'))
    .pipe(gulp.dest(bases.dist + 'js/'))
    .pipe(livereload());
};
gulp.task('js', ['clean'], js);
gulp.task('js-watch', js);

gulp.task('watch', function () {
  livereload.listen();
  gulp.watch(paths.styles, ['sass-watch']);
  gulp.watch(paths.js, ['js-watch']);
  gulp.watch(paths.files.files, ['files-watch']);
  gulp.watch(paths.files.images, ['images-watch']);
  gulp.watch(paths.vendor_js, ['vendor-js-watch']);
  gulp.watch(paths.vendor, ['vendor-watch']);

  /* Trigger update on changes in Django Templates */
  // gulp.watch('**/*/templates/*').on('change', livereload.changed);
});

gulp.task('build', ['clean', 'sass', 'js', 'vendor', 'vendor-js', 'files', 'images']); // Build all
gulp.task('watch-dev', ['build', 'watch']); // Run build, then watch
gulp.task('default', ['build', 'watch']); // Run build, then watch
