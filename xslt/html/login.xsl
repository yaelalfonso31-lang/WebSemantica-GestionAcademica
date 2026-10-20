<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:import href="layout.xsl"/>

    <!-- Los errores de acceso llegan como alertas flash (las inyecta el transformador en <main>). -->
    <xsl:template name="content">
        <div class="container py-5">
            <div class="row justify-content-center">
                <div class="col-11 col-sm-8 col-md-6 col-lg-4">
                    <div class="card shadow-sm border-0 border-top border-primary border-4">
                        <div class="card-body p-4">
                            <h2 class="fw-bold mb-1">Acceso al sistema</h2>
                            <p class="text-muted mb-4">Ingresa con tu usuario institucional.</p>

                            <form action="/login" method="POST">
                                <div class="mb-3">
                                    <label for="username" class="form-label fw-semibold">Usuario</label>
                                    <input type="text" id="username" name="username" class="form-control"
                                           required="required" autofocus="autofocus" autocomplete="username"/>
                                </div>
                                <div class="mb-4">
                                    <label for="password" class="form-label fw-semibold">Contraseña</label>
                                    <input type="password" id="password" name="password" class="form-control"
                                           required="required" autocomplete="current-password"/>
                                </div>
                                <button type="submit" class="btn btn-primary w-100 fw-bold py-2">Ingresar</button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>
