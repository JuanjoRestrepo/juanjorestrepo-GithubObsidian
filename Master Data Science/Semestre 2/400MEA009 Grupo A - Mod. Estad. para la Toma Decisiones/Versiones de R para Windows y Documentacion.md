

# Previous Releases of R for Windows
https://cran.r-project.org/bin/windows/base/old/


1. Remove any existing (possibly incomplete) installation
```R
remove.packages("stringi")
```

2. Install the binary version of the package
```R
install.packages("stringi", type = "binary")
```

3. Verify the package installation on Console
```R
library(stringi)
```

4. (Optional) Check your *Rtools* installation
```R
# Install pkgbuild if not already installed
if (!requireNamespace("pkgbuild", quietly = TRUE)) {
  install.packages("pkgbuild")
}
pkgbuild::find_rtools()
```

