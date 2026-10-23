# Run with: Rscript -e 'testthat::test_dir("r/tests/testthat")'
lib <- normalizePath(file.path("..", "..", "..", "src", "repro_check", "engines", "qtl2", "lib.R"),
                     mustWork = FALSE)
if (!file.exists(lib)) lib <- normalizePath("src/repro_check/engines/qtl2/lib.R")
source(lib)

test_that("rankz keeps NA and gives a standard normal shape", {
  z <- rankz(c(3, NA, 1, 2))
  expect_true(is.na(z[2]))
  expect_equal(z[c(3, 4, 1)], qnorm(c(0.5, 1.5, 2.5) / 3))
})

test_that("log transform drops non-positive values and counts them", {
  x <- transform_trait(c(1, 0, -2, exp(1)), "log")
  expect_equal(as.numeric(x), c(0, NA, NA, 1))
  expect_equal(attr(x, "n_nonpositive"), 2)
  expect_error(transform_trait(1, "sqrt"), "unknown transform")
})

test_that("addcovar keeps row order and NA rows, expands factors", {
  covar <- data.frame(sex = c("F", "M", "F", "M"), wave = c(1, 2, NA, 3),
                      row.names = c("a", "b", "c", "d"))
  m <- build_addcovar(covar, c("sex", "wave"), factors = "wave")
  expect_equal(rownames(m), c("a", "b", "c", "d"))
  expect_equal(colnames(m), c("sexM", "wave2", "wave3"))
  expect_true(all(is.na(m["c", ])))
  expect_equal(unname(m["d", ]), c(1, 0, 1))
  expect_error(build_addcovar(covar, "diet"), "not found")
})

# Two chromosomes so LOCO kinship is defined; founders drawn per individual
# per chromosome (no recombination), which is enough to test the plumbing.
make_cross <- function(n = 200, n_mark = 60, seed = 1) {
  set.seed(seed)
  chrs <- c("1", "2")
  map <- lapply(chrs, function(ch) setNames(seq(1, n_mark), sprintf("c%s_m%02d", ch, seq_len(n_mark))))
  names(map) <- chrs
  probs <- lapply(chrs, function(ch) {
    arr <- array(0, c(n, 8, n_mark), dimnames = list(sprintf("i%03d", 1:n), LETTERS[1:8], names(map[[ch]])))
    for (i in 1:n) {
      f1 <- sample(8, 1); f2 <- sample(8, 1)
      arr[i, f1, ] <- arr[i, f1, ] + 0.5
      arr[i, f2, ] <- arr[i, f2, ] + 0.5
    }
    arr
  })
  names(probs) <- chrs
  attr(probs, "crosstype") <- "do"
  attr(probs, "is_x_chr") <- c("1" = FALSE, "2" = FALSE)
  attr(probs, "alleles") <- LETTERS[1:8]
  attr(probs, "alleleprobs") <- TRUE
  class(probs) <- c("calc_genoprob", "list")
  list(probs = probs, map = map)
}

test_that("peaks_with_effects finds a planted effect and its founder", {
  x <- make_cross()
  y <- matrix(2 * x$probs[["1"]][, "F", "c1_m30"] + rnorm(200), ncol = 1,
              dimnames = list(rownames(x$probs[["1"]]), "y"))
  k <- calc_kinship(x$probs, "loco")
  s <- scan1(x$probs, y, kinship = k)
  pk <- peaks_with_effects(s, x$probs, y, k, NULL, x$map, threshold = 3, peakdrop = Inf, drop = 1.5)
  expect_length(pk, 1)
  expect_equal(pk[[1]]$chr, "1")
  coef <- unlist(pk[[1]]$coef)
  expect_equal(names(which.max(coef)), "F")
})

test_that("write_profile writes one row per marker", {
  x <- make_cross(n = 50, n_mark = 10)
  y <- matrix(rnorm(50), ncol = 1, dimnames = list(rownames(x$probs[["1"]]), "y"))
  s <- scan1(x$probs, y)
  f <- tempfile(fileext = ".csv.gz")
  write_profile(s, x$map, f)
  d <- read.csv(gzfile(f))
  expect_equal(nrow(d), 20)
  expect_equal(colnames(d), c("marker", "chr", "pos", "y"))
})
