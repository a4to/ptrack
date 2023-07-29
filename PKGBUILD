# Maintainer: Connor Etherington <connor@concise.cc>
# ---
pkgname=ptrack
pkgver=0.1.0
pkgrel=1
pkgdesc="A simple CLI utility for asthetically tracking progress when copying or moving files"
arch=(x86_64)
url="https://gitlab.com/a4to/${pkgname}"
license=('MIT')
depends=(
  "python3"
  "python-argparse"
  "python-rich"
  "python-argcomplete"
  "python-setuptools"
)
source=(
  "https://concise.cc/pkg/${pkgname}-${pkgver}-${pkgrel}-$arch.pkg.tar.xz"
)
sha512sums=(
  'b64b804dbfd5e36c63e154babc323b2f8c0e31cbb889019637a6e27aa609e3f85260d7e17d777ca3348862e3d0f23ec88085c34a0e58c98069df733dd470bd22'
)
md5sums=(
  '662515fdc899d59e6fef3313a292c953'
)
validpgpkeys=(
  '81BACEEBC3EA26E127166E4A819BB92A9A48160E'
)

package() {

  cd "$srcdir/${pkgname}-${pkgver}-${pkgrel}-${arch}" ||
  cd "$srcdir/${pkgname}"

  python3 ./setup.py install --root="$pkgdir" --prefix=/usr --optimize=1

  install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
  install -Dm644 README.md "${pkgdir}/usr/share/doc/${pkgname}/README.md"

}
